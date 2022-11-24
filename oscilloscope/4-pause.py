#!/usr/bin/python3

import subprocess
import numpy as np
import pandas as pd
import pdb
import socket, sys, os, time, threading
from struct import pack

from datoviz import canvas, run, colormap

#Set up graph background
c = canvas(show_fps=True)
s = c.scene()
gui = c.gui("GUI")
panel = s.panel(controller='axes')
visual = panel.visual('path')

# Initialise global variables - global variables required because datoviz calls functions automatically and so these cannot be passed as argument.
lag = 0 # How far behind the most recent sample the start of the viewing window is
pause = False # whether or not the oscilloscope is paused
start = 0 # How far from the first sample the start of the viewing window is
width = 200 # Number of samples in the viewing window
freq = 10000 # Set the frequency of the wave produced in the waveform generator
amp = 1 # Set the amplitude of the wave produced in the waveform generator
wave = 0 # Set the shape of the wave produced in the waveform generator (0 = Sine, 1 = Square, 2 = Saw.)

# Describe buttons and sliders on the GUI
timebase = gui.control("slider_int", "Timebase", vmin=10, vmax=2000) # Change width of viewing window
frequency = gui.control("slider_int", "frequency", vmin=1000, vmax=20000)
amplitude = gui.control("slider_float", "Amplitude", vmin=0.1, vmax=10.0)
sine = gui.control("button", "Sine wave")
square = gui.control("button", "Square wave")
saw = gui.control("button", "Saw wave")
hold = gui.control("button", "| |") # Pause the oscilloscope
left = gui.control("button", "<---") # Move the viewing window left by half a window
right = gui.control("button", "--->") # Move the viewing window right by half a window
track = gui.control("button", "Live") # Go the most recent sample

# Function to communicate a change in waveform to the waveform generator via UDP
def waveEdit(wave1=0, gain1=1, freq1=10000, wave2=0, gain2=1, freq2=1):
    port = 5432     #arbitrary port
    ip = "127.0.0.1"

    args = ["IfIIfI", int(wave1), float(gain1), int(freq1), int(wave2), float(gain2), int(freq2)]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(pack(*args), (ip, port))

# All of these decorators trigger when the connected GUI element is changed.
@timebase.connect
def on_change(value):
    global width
    width = value

@frequency.connect
def on_change(value):
    global freq
    freq = value

@amplitude.connect
def on_change(value):
    global amp
    amp = value

@sine.connect
def on_change(value):
    global wave, freq, amp
    print("Frequency = {}".format(freq))
    wave = 0
    waveEdit(wave, amp, freq)

@square.connect
def on_change(value):
    global wave, freq, amp
    wave = 1
    waveEdit(wave, amp, freq)

@saw.connect
def on_change(value):
    global wave, freq, amp
    wave = 2
    waveEdit(wave, amp, freq)

@hold.connect
def on_change(value):
    global pause, start, lag, width
    if pause == False:
        pause = True
        live = int(subprocess.getoutput('wc -l < ../data/wave.csv')) # Number of lines = number of samples
        start = live - lag - width # start = current position
        print("Time is {}. Pausing...".format(start))
    else:
        print("Resuming...")
        pause = False

@left.connect
def on_change(value):
    global start, lag, width
    lag = int(lag + (width / 2))
    start = int(start - (width / 2))

@right.connect
def on_change(value):
    global start, lag, width
    lag = int(lag - (width / 2))
    start = int(start + (width / 2))

@track.connect
def on_change(value):
    global start, lag, width
    live = int(subprocess.getoutput('wc -l < ../data/wave.csv'))
    lag = width
    start = live - width

@c.connect
def on_frame(i):
    # This function runs at every frame.
    global width, start, pause, lag
    live = int(subprocess.getoutput('wc -l < ../data/wave.csv'))

# Guards to keep window in bounds of the array of samples
    if width > live:
        width = live
        lag = 0

    if lag < width:
        lag = width
    if lag > live:
        lag = live

    if start + width > live:
        start = live - width
    if start < 0:
        start = 0

# Normally count back from the most recent sample because it's easier than keeping count of the start position as it moves
    if pause == False:
        csv = subprocess.getoutput('tail -n {} ../data/wave.csv | head -n {}'.format(lag + width, width))
    else:
# When paused, count forwards from 0 so we still don't need to keep track of the moving current position
        csv = subprocess.getoutput('head -n {} ../data/wave.csv | tail -n {}'.format(start + width, width))

    csv = csv.splitlines()[0:-2] # Trim the last couple of lines because they are usually partially written.
    Y = [line.split(',')for line in csv] # Tokenise CSV
    df = pd.DataFrame(Y) # Pandas probably not necessary but I wanted to experiment with it

    print(df)

    pos = [] # list of 3D co-ordinates for each point in the graph, in the format (X, Y, Z)
    for x in range(len(df.index)):
        pos.append([df.iloc[x, 0], df.iloc[x, 1], 0]) # Create the tuple of X, Y, Z co-ords and add it to the list

    pos = np.array(pos)
    visual.data('pos', pos) # Assign the points to the graph and run

run()
