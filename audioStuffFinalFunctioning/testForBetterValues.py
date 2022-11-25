import goertzel, pyaudio, time, Important, logging, progressbar, pysine, wave, struct
from threading import Thread
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

delay = 2
frequencyPlay = 775
frequencyListen = 800
threshhold = 70_000_000 # Long Distance falloff 474_923_015
threshhold = 250_000_000
timePlaying = 2
velocity = 343 


#AUDIO INPUT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100 # 44100
CHUNK = 1024 * 176 # RATE * (timeRecording + delay)
realChunk = 1024 * 2
timeSoundPlayedAt = -1

windowSize = 1 / RATE

audio = pyaudio.PyAudio()

def writeToFile(fileName, chunk): 
    wf = wave.open(fileName, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(chunk)
    wf.close()




stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK, input_device_index=1)


def threadPlaySound(freqsss, timePlay):
    global timeSoundPlayedAt
    time.sleep(delay)
    timeSoundPlayedAt = time.time_ns()
    pysine.sine(frequency=freqsss, duration=timePlay)
    timeSoundPlayedAt = timeSoundPlayedAt
    print("Sound Played")

threadPlayer = Thread(target=threadPlaySound, args=((frequencyPlay, timePlaying)))
threadPlayer.start()

print("Start recording")
timeRecordingStart = time.time_ns()
hugeChunk = stream.read(CHUNK)
print("End recording")


freqs = (frequencyListen, frequencyListen)

frameFoundAt = 0

bar = progressbar.ProgressBar(max_value=CHUNK)

searchTillEnd = True

maxValue = 0
frameMaxAt = 0

trueChunk = struct.unpack(str(2 * CHUNK) + 'B', hugeChunk)
chunkNumpy = np.array(trueChunk, dtype='B')[::2] + 128
vals = []


fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
fig.show()
xf = np.linspace(0, RATE, realChunk)     # frequencies (spectrum)
line_fft, = ax2.semilogx(xf, np.random.rand(realChunk), '-', lw=2)
ax2.set_xlim(20, RATE / 2)



for i in range(0, CHUNK - realChunk): 
    bar.update(i)
    chunkRightNow = chunkNumpy[i:i+realChunk*2]
    fftVals = np.abs(fft(chunkRightNow)[0:realChunk]) * 2 / (128 * realChunk)
    line_fft.set_ydata(fftVals)
    #fig.canvas.draw()
    #fig.canvas.flush_events()
    

    

# for i in range(CHUNK - realChunk):
#     bar.update(i)
#     chunkRightNow = hugeChunk[i:i+realChunk]
#     data = struct.unpack(str(2 * realChunk) + 'B', chunkRightNow)
#     print(data)
#     if False:
#         freqss, value = Important.calculateFromChunk(chunkRightNow, freqs)
#         value = value[0][2]
#         if (maxValue < value): 
#             maxValue = value
#             frameMaxAt = i


#         if (value > threshhold and val):
#             frameFoundAt = i - realChunk
#             if (searchTillEnd): 
#                 print("Found on Chunk from frame: " + str(i) + " to: " + str(i + realChunk))
#                 val = False
#             else: 
#                 break
print("")
timeDistance = frameFoundAt / RATE # = 0
print(timeDistance)
timeRec = timeRecordingStart + timeDistance
timeSoundPlayedAt /= 1e+18
timeRec /= 1e+18
print("Time Based of recording: ", timeRec)
print("Time Based of TimeSoundPlayed: ", timeSoundPlayedAt)
print("Max Loudness Heard:", maxValue, "; at: ", frameMaxAt) # Use this line to get information about possible threshhold


deltaTime = timeRec - timeSoundPlayedAt
print("Distance Caclulated: ", deltaTime)