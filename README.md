----\_\_\_\_---\_\_\_--\_\_-\_MARTePlot\_-\_\_--\_\_\_---\_\_\_\_----
=====================================================================

MARTePlot is a digital waveform generator and oscilloscope powered by [MARTe2](https://vcis.f4e.europa.eu/marte2-docs/master/html/). This repository contains several variations on this idea, to fit a variety of use cases. Please reach out with code for anything in the below list of planned variations or ideas for things that aren't on the list.

The repository is split into different directories for waveformGenerators and oscilloscopes, with the hope that different generators can be paired with different scopes as required. The variations are enumerated in the order that I complete them, which is loosely in the order of complexity.

Waveform Generators
-------------------

| Variation | Overview |
|-----------|----------|
| [1-CSV](waveformGenerator/1a-HardCodedParams/README.md) | A minimal implementation of sine, square and saw wave generators. Amplitude, frequency and wave type can be toggled live. Data is written into a CSV file. |
| 2-TwoChannel | This implementation writes two channels consecutively |
| 3-LowMemory | Data is not stored, only the previous n values are kept as a circular buffer |
| 4-PythonGenerated | The configuration files are generated in Python, which allows for control of things that were previously hard coded into the .cfg file |
| 5-NChannel | Python generation allows for the number of channels to be variable |

Oscilloscopes
-------------

| Variation | Overview |
|-----------|----------|
| [1-StaticMatplot](waveformGenerator/1a-HardCodedParams/README.md) | Draws frames in MatPlotLib to give illusion of animation. Reads 1 channel from CSV. |
| 2-GeneralMatPlot | Draws frames in MatPlotLib to give illusion of animation. Analyses CSV files to handle various data formats. |
| 3-Animated | Attempt to better optimise drawing by only drawing most recently updated points to the right of the screen. |
| x-MatLabIntegration | Use MATLab to chart the points by importing from a CSV. |
| x-jScope | Store data in an MDSPlus tree to make use of jScope as a plotting tool |
| x-PausableStream | Look into how triggers might be able to pause the animation, allow the user to zoom into data points live. |
| x-gui | Change parameters in Waveform generator using an integrated GUI | 
