#!/usr/bin/python3

import subprocess
import numpy as np
import pandas as pd
import pdb

from datoviz import canvas, run, colormap

c = canvas(show_fps=True)
s = c.scene()
panel = s.panel(controller='axes')
visual = panel.visual('path')

@c.connect
def on_frame(i):
    # This function runs at every frame.

    live = int(subprocess.getoutput('wc -l < ../data/wave.csv'))
    lag = 100
    width = 11
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
