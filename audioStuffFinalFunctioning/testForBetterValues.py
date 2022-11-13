import goertzel, pyaudio, time, Important, logging, progressbar
from threading import Thread
import numpy as np
import matplotlib.pyplot as plt
import pysine

time.sleep(3)

delay = 2
frequency = 689
threshhold = 70_000_000 # Long Distance falloff
timeRecording = 3

#AUDIO INPUT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100 # 44100
CHUNK = RATE * (timeRecording + delay)
realChunk = 1024

def threadPlaySound(freqsss, timePlay):
    time.sleep(delay)
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


audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK, input_device_index=1)


threadPlayer = Thread(target=threadPlaySound, args=((frequency, 1.0)))
threadPlayer.start()

print("Start recording")
hugeChunk = stream.read(CHUNK)
print("End recording")

freqs = (frequency, frequency)

frameFoundAt = 0

bar = progressbar.ProgressBar(max_value=CHUNK)

searchTillEnd = False

maxValue = 0
frameMaxAt = 0

val = True
for i in range(CHUNK - realChunk):
    bar.update(i)
    chunkRightNow = hugeChunk[i:i+realChunk]
    freqss, value = Important.calculateFromChunk(chunkRightNow, freqs)
    value = value[0][2]
    if (maxValue < value): 
        maxValue = value
        frameMaxAt = i

    if (value > threshhold and val):
        frameFoundAt = i
        if (searchTillEnd): 
            print("Found on Chunk from frame: " + str(i) + " to: " + str(i + realChunk))
            val = False
        else: 
             break

print("")
timeDistance = frameFoundAt / RATE - delay# = 0
print("Max Loudness Heard:", maxValue, "; at: ", frameMaxAt)
print("Time heard: ", timeDistance)