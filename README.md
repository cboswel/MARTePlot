-----_____----____---___--__-_MARTePlot_-__--___---____----_____-----
=====================================================================

MARTePlot is a digital waveform generator and oscilloscope powered by [MARTe2](https://vcis.f4e.europa.eu/marte2-docs/master/html/). This repository contains several variations on this idea, to fit a variety of use cases. Please reach out with code for anything in the below list of planned variations or ideas for things that aren't on the list.

The repository is split into different directories for waveformGenerators and oscilloscopes, with the hope that different generators can be paired with different scopes as required. The variations are enumerated in the order that I complete them, which is loosely in the order of complexity.

Waveform Generators
-------------------

| Variation | Overview |
|-----------|----------|
| [1-CSV](waveformGenerator/1a-HardCodedParams/README.md) | A minimal implementation of sine, square and saw wave generators. Amplitude, frequency and wave type can be toggled live. Data is written into a CSV file. |
| 2-TwoChannel | This implementation writes two channels consecutively |
| 3-LowMemory | Data is not stored, only the previous n values are kept as a circuler buffer |
| 4-PythonGenerated | The configuration files are generated in Python, which allows for control of things that were previously hard coded into the .cfg file |
| 5-NChannel | Python generation allows for the number of channels to be variable |


