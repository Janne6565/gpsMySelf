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
realChunk = int(1024 / 2)
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
    print("Sound Played")

threadPlayer = Thread(target=threadPlaySound, args=((frequencyPlay, timePlaying)))
threadPlayer.start()

print("Start recording")
timeRecordingStart = time.time_ns()
hugeChunk = stream.read(CHUNK)
timeRecordingEnd = time.time_ns()
print("End recording")

timeTillRecordingRealStarted = ((timeRecordingEnd - timeRecordingStart) * 1e-9) - (CHUNK / RATE)


freqs = (frequencyListen, frequencyListen)

frameFoundAt = 0

bar = progressbar.ProgressBar(max_value=CHUNK)

searchTillEnd = True

maxValue = 0
frameMaxAt = 0

wf_data = np.frombuffer(hugeChunk, dtype='h')  
data_int = np.array(wf_data, dtype='h')/140 + 255
vals = []


fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
fig.show()
xf = np.linspace(0, RATE, realChunk)     # frequencies (spectrum)
line_fft, = ax2.semilogx(xf, np.random.rand(realChunk), '-', lw=2)
ax2.set_xlim(20, RATE / 2)


indexOfFrequency = int((frequencyListen - (frequencyListen % (RATE / realChunk))) / (RATE/realChunk))
print(indexOfFrequency)


frameFoundAt = -1
threshhold = 0.01
arr = []

for i in range(0, CHUNK - realChunk): 
    bar.update(i)
    chunkRightNow = data_int[i:i+realChunk*2]
    fftVals = np.abs(fft(chunkRightNow)[0:realChunk]) * 2 / (128 * realChunk)
    line_fft.set_ydata(fftVals)
    value = fftVals[indexOfFrequency]
    arr.append(fftVals[indexOfFrequency])

    if (value > threshhold):
        frameFoundAt = i
        print("Found on ", i)
        break
    if False: # If you want to see the Data on a graph (very slow)
        fig.canvas.draw()
        fig.canvas.flush_events()

print("Max value:", max(arr))

print("TimeTillRecordingRealStarted:",timeTillRecordingRealStarted)
timeDistance = ((frameFoundAt / RATE) + timeTillRecordingRealStarted) * 1e+9
print("TimeDistance:", timeDistance)

timeUntilSoundPlayed = timeSoundPlayedAt - timeRecordingStart
print("TimeUntilSoundPlayed", timeUntilSoundPlayed)

timeRec = timeDistance - timeUntilSoundPlayed
print("TimeRec", timeRec)


relativeTime = abs(timeRec) * 1e-9

print("Relative Time: ", relativeTime)


distance = relativeTime * velocity
print("Distance: ", distance)