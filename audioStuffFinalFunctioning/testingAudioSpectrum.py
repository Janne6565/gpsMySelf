# Credits: https://www.youtube.com/watch?v=aQKX3mrDFoY 
# Video über Audio Spektrum

import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time
from tkinter import TclError

# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second
# create matplotlib figure and axes
fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
fig.show()
# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)
print(max(xf))
print(xf)
count = 0
for i in xf: 
    if (780 < i < 820):
        print(i)
        print(count)
    count += 1
# create a line object with random data
line, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)

# create semilogx line for spectrum
line_fft, = ax2.semilogx(xf, np.random.rand(CHUNK), '-', lw=2)

# format waveform axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('volume')
ax1.set_ylim(0, 255)
ax1.set_xlim(0, 2 * CHUNK)
plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

# format spectrum axes
ax2.set_xlim(20, RATE / 2)

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()

frequencyListenTo = 10000
oldFrame = time.time_ns()
newFrame = time.time_ns()
while True:
    oldFrame = time.time_ns()
    print(oldFrame - newFrame)

    newFrame = oldFrame
    # binary data
    data = stream.read(CHUNK)  
    # convert data to integers, make np array, then offset it by 127
    wf_data = np.frombuffer(data, dtype='h')  
    data_int = np.array(wf_data, dtype='h')/140 + 255
    # create np array and offset by 128
    
    line.set_ydata(data_int)
    
    # compute FFT and update line
    yf = fft(data_int)
    realYData = np.abs(yf[0:CHUNK])  / (128 * CHUNK)
    # print("AVG", sum(realYData[10:-1])/len(realYData[10:-1]), "realData:", realYData[37])


    indexOfFrequency = int((frequencyListenTo - (frequencyListenTo % (RATE / CHUNK))) / (RATE/CHUNK)) # Calculating index of frequency we want to listen to


    line_fft.set_ydata(realYData)
    
    # update figure canvas

    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1
        
    except TclError:
        
        # calculate average frame rate
        frame_rate = frame_count / (time.time() - start_time)
        
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break