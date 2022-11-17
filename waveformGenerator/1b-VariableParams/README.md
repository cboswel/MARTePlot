1-CSV
=====

This is version 0.1 of the MARTe2 signal generator. It works by using the WaveformGAM to generate a sine, square and saw wave. These are all then sent through a multiplexer to let the user switch between them while the application is running. In the final verison, 8-variable, the amplitude and period of the wave can be changed live as well. These live changes are done by sending a UDP packet through localhost, which is picked up and read by MARTe. 

To send a comand through UDP, run the bash script `./tweak` with three arguments:

1. Wave select - This is an integer, 0 1 or 2, to select the type of waveform displayed. 0 is a sine wave, 1 is a square wave and 2 is a saw wave.
2. Amplitude - This is a float that represents the peak amplitude of the wave.
3. Frequency - This is an integer that represents the frequency of the wave. A value of 1 represents 1/1,000,000 Hz if MARTe updates at 1Hz. The program is currently set to update at 100Hz. The bounds for this value are therefore between 1, where it will take 1,000,000 program cycles to complete a wave, and 500,000, at which point each wave will only be sampled two times.

For example, running `./tweak 1 2 10000` would generate a square wave with peak amplitude 2 and a frequency of 1/100 Hz in terms of program cycles.

Versions 4 - 6 only accept one argument, to select the waveform. Versions 5 and 6 offer the ability to change the amplitude and period respectively, but this is hard coded in the .cfg file. Version 7 works by taking three arguments, as mentioed above.
