import goertzel, pyaudio, time, Important, logging
from threading import Thread
import numpy as np
import matplotlib.pyplot as plt
import pysine

def threadPlaySound(freqsss, timePlay):
    time.sleep(0.4)
    pysine.sine(frequency=freqsss, duration=timePlay)
    print("Sound Played")

def threadListenSound(freqs, threshhold):
    timeStart = time.time_ns() + 1 * 10 ** 9
    while True: 
        freqss, vals = Important.getVals(freqs)
        vals = vals[0]
        print(vals[2])
        if (vals[2] > threshhold): 
            timeNow = time.time_ns()
            print((timeNow - timeStart) / 10**9)
            return timeStart - timeNow


#threadListener = threading.Thread(target=threadListenSound((796, 796), 10*10**20))
#threadPlayer = threading.Thread(target=threadPlaySound(796.0, 1.0))
#listenSoundThread = Thread(target=threadListenSound, args=((900, 900), 10**9))
#listenSoundThread.start()

#time.sleep(1)

threadPlayer = Thread(target=threadPlaySound, args=((600, 1.0)))


#AUDIO INPUT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = RATE * 4
realChunk = 1024


audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

threadPlayer.start()

print("Start recording")
hugeChunk = stream.read(CHUNK)
print("End recording")

freqs = (600, 600)
threshhold = 4 * 10**8

frameFoundAt = -1

for i in range(CHUNK - realChunk):
    chunkRightNow = hugeChunk[i:i+realChunk]
    freqss, value = Important.calculateFromChunk(chunkRightNow, freqs)
    value = value[0][2]
    if (value > threshhold):
        frameFoundAt = i
        print("Found on Chunk from frame: " + str(i) + " to: " + str(i + realChunk))
        break


timeDistance = frameFoundAt / RATE
print(timeDistance)