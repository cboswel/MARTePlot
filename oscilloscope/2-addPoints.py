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

global history
history = pd.DataFrame()

@c.connect
def on_frame(i):
    # This function runs at every frame.
#    csv = subprocess.getoutput('tail -n -20 ../data/wave.csv')
#    csv = csv.splitlines()
#    df = pd.DataFrame([csv])

    csv = subprocess.getoutput('tail -n -20 ../data/wave.csv')
    csv = csv.splitlines()[0:-2]
    Y = [line.split(',')for line in csv]
    df = pd.DataFrame(Y)

#    df = pd.read_csv('../data/wave.csv')
    global history
    history = pd.concat([history, df]).drop_duplicates().reset_index(drop=True)

    length = np.repeat(np.array([len(history)]), 2)

    pos = []
    for x in range(len(history)):
        pos.append([history.iloc[x, 0], history.iloc[x, 1], 0])
    for x in range(len(history)):
        pos.append([history.iloc[x, 0], history.iloc[x, 2], 0])

    pos = np.array(pos)
    visual.data('pos', pos)
    visual.length('length', length)

run()
