#!/usr/bin/python3

import matplotlib.pyplot as plt
import subprocess
import numpy as np

from datoviz import canvas, run, colormap

c = canvas()
s = c.scene()
panel = s.panel(controller='axes')
visual = panel.visual('path')

@c.connect
def on_frame(i):
    # This function runs at every frame.
    output = subprocess.getoutput('tail -n -200 ../data/wave.csv')
    Y = output.splitlines()[0:-1]
    Y = [float(line) for line in Y]

    pos = []
    for x in range(199):
        pos.append([x, Y[x], 0])

    pos = np.array(pos)
    visual.data('pos', pos)

run()
