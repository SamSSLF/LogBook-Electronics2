from mic import MICROPHONE
from pyb import Pin, Timer, ADC, DAC, LED

SAMP_FREQ = 8000
N = 160
mic = MICROPHONE(Timer(7,freq=SAMP_FREQ),ADC('Y11'),N)
samples = mic.read()
plot(samples,SAMP_FREQ)