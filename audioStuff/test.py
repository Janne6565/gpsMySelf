import numpy as np #importing Numpy with an alias np
import pyaudio as pa 
import struct, time
import matplotlib.pyplot as plt
import sounddevice as sd

def drawData(data): 
    line.set_ydata(data)
    fftData = np.abs(np.fft.fft(data))*2/(11000*CHUNK)
    line_fft.set_ydata(fftData)
    fig.canvas.draw()
    fig.canvas.flush_events()

def makePos(num): 
    if (num < 0): 
        return num * -1
    else: 
        return num

CHUNK = 1024 * 1
FORMAT = pa.paInt16
CHANNELS = 1
RATE = 44100 # in Hz

p = pa.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)



fig, (ax,ax1) = plt.subplots(2)
x_fft = np.linspace(0, RATE, CHUNK)
x = np.arange(0,2*CHUNK,2)
line, = ax.plot(x, np.random.rand(CHUNK),'r')
line_fft, = ax1.semilogx(x_fft, np.random.rand(CHUNK), 'b')
ax.set_ylim(-2000,2000)
ax.ser_xlim = (0,CHUNK)
ax1.set_xlim(20,RATE/2)
ax1.set_ylim(0,0.2)
fig.show()

while 1:
    timeBefore = time.time_ns()
    data = stream.read(CHUNK)
    dataInt = struct.unpack(str(CHUNK) + 'h', data)
    print(makePos(dataInt[800]))
    drawData(dataInt)