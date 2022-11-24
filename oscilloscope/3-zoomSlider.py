#!/usr/bin/python3

import subprocess
import numpy as np
import pandas as pd
import pdb
import socket, sys, os, time, threading
from struct import pack

from datoviz import canvas, run, colormap

c = canvas(show_fps=True)
s = c.scene()
gui = c.gui("GUI")
panel = s.panel(controller='axes')
visual = panel.visual('path')

live = int(subprocess.getoutput('wc -l < ../data/wave.csv'))
lag = 0
width = 200
freq = 10000
amp = 1
wave = 0

timebase = gui.control("slider_int", "Timebase", vmin=10, vmax=2000)
sine = gui.control("button", "Sine wave")

def waveEdit(wave1=0, gain1=1, freq1=10000, wave2=0, gain2=1, freq2=1):
    port = 5432     #arbitrary port
    ip = "127.0.0.1"

    args = ["IfIIfI", int(wave1), float(gain1), int(freq1), int(wave2), float(gain2), int(freq2)]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(pack(*args), (ip, port))

@timebase.connect
def on_change(value):
    global width
    width = value

@sine.connect
def on_change(value):
    global wave, freq, amp
    print("Frequency = {}".format(freq))
    wave = 0
    waveEdit(wave, amp, freq)

@c.connect
def on_frame(i):
    # This function runs at every frame.

    global width

    live = int(subprocess.getoutput('wc -l < ../data/wave.csv'))
    lag = 100
    if width > live:
        width = live
        lag = 0
    if lag + width > live:
        lag = live - width

    csv = subprocess.getoutput('tail -n {} ../data/wave.csv | head -n {}'.format(lag + width, width))
    csv = csv.splitlines()[0:-2]
    Y = [line.split(',')for line in csv]
    df = pd.DataFrame(Y)

#    length = np.repeat(np.array([len(history)]), 2)

    pos = []
    for x in range(len(df.index)):
        pos.append([df.iloc[x, 0], df.iloc[x, 1], 0])

    pos = np.array(pos)
    visual.data('pos', pos)
    print(df.iloc[len(df.index)] - 1, subprocess.getoutput('tail -n 1 ../data/wave.csv'))
#    visual.length('length', length)

run()
