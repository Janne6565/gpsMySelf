import pyaudio, goertzel, time
import numpy as np
import matplotlib.pyplot as plt

#AUDIO INPUT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

def getVals(freqs): 
    inputt = stream.read(CHUNK) 
    freqs, results = goertzel.goertzel(inputt, RATE, (freqs[0], freqs[1]))
    return freqs, results

#x = np.linspace(1, 2, 3)
#y = np.linspace(1, 2, 3)
#plt.ion()
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.set_ylim(100)
#line1, = ax.plot(x, y, 'r-')

while True:
    freqs, results = getVals((800, 800))
    res = np.array(results)[:,2]
    realResult = res / 100000000
    if (realResult >= 10):
        print("Called")
    #line1.set_ydata(y)
    #fig.canvas.draw()
    #fig.canvas.flush_events()


# Measure Time
#timeBefore = time.time()
#print(timeBefore)
#for i in range(1000):
#    inputt = stream.read(CHUNK)
#    if (i % 100 == 0):
#        print(i)
#
#timeAfter = time.time()
#
#
#print((timeAfter-timeBefore) / 1000)

#print([results[0][0], results[0][1], results[0][2]])
#plt.plot([1, 2, 3], [results[0][0], results[0][1], results[0][2]], 'ro')
#plt.axis([1, 3, 0, 1000000])
#plt.show()