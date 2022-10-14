#!/bin/python3

import matplotlib.pyplot as plt
import subprocess

output = subprocess.getoutput('tail -n -200 ../data/wave.csv')
Y = output.splitlines()[0:-1]
Y = [float(line) for line in Y]

plt.ion()
graph = plt.plot(Y)[0]
plt.axis([0, 200, -1, 1])
plt.ylabel('amplitude')

while True:

    output = subprocess.getoutput('tail -n -200 ../data/wave.csv')
    Y = output.splitlines()[0:-1]
    Y = [float(line) for line in Y]
    graph.set_ydata(Y)
    plt.draw()
    plt.pause(0.011)
