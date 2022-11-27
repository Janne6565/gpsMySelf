import goertzel, pyaudio, time, Important, logging, progressbar, pysine, wave, struct
from threading import Thread
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

delay = 2
frequencyPlay = 775
frequencyListen = 800
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


def getDistanceToSpeaker(STREAM, CHUNK, REALCHUNK, FREQUENCYPLAY, TIMEPLAYING, DEBUG, VELOCITY, THRESHHOLD): # Function to calculate Distance from Speaker and Microphone
    threadPlayer = Thread(target=threadPlaySound, args=((FREQUENCYPLAY, TIMEPLAYING)))
    threadPlayer.start()

    print("Start recording")
    timeRecordingStart = time.time_ns() # Messuring recording time
    hugeChunk = STREAM.read(CHUNK)
    timeRecordingEnd = time.time_ns()
    print("End recording")

    timeTillRecordingRealStarted = ((timeRecordingEnd - timeRecordingStart) * 1e-9) - (CHUNK / RATE)

    frameFoundAt = 0

    bar = progressbar.ProgressBar(max_value=CHUNK)

    readData = np.frombuffer(hugeChunk, dtype='h')  # Converting Chunk to readable Chunk
    readData = np.array(readData, dtype='h')/140 + 255
    vals = []

    indexOfFrequency = int((frequencyListen - (frequencyListen % (RATE / REALCHUNK))) / (RATE/REALCHUNK)) # Calculating index of frequency we want to listen to

    frameFoundAt = -1
    arr = []

    for i in range(0, CHUNK - REALCHUNK): # Checking through all sub-chunks, detects first 
        bar.update(i)
        chunk = readData[i:i+REALCHUNK*2]
        realValues = np.abs(fft(chunk)[0:REALCHUNK]) * 2 / (128 * REALCHUNK)
        valueOfFrequency = realValues[indexOfFrequency]
        arr.append(realValues[indexOfFrequency])

        if (valueOfFrequency > THRESHHOLD):
            frameFoundAt = i
            break


    timeDistance = ((frameFoundAt / RATE) + timeTillRecordingRealStarted) * 1e+9 # Time (relative) we heard the sound at (correction for delay in the STREAM.READ() methode) (ns)
    timeUntilSoundPlayed = timeSoundPlayedAt - timeRecordingStart # Time (relative) we heard the sound at (ns)
    timeRec = timeDistance - timeUntilSoundPlayed # Time (relative) it took the sound to travel to the microphone (ns)
    relativeTime = abs(timeRec) * 1e-9 # Time (relative) it took the sound to travel to the microphone (s)
    distance = relativeTime * VELOCITY # Distance calculated by the time the sound traveled 

    if (DEBUG): 
        print("Max value:", max(arr))
        print("Found on:", frameFoundAt)
        print("TimeTillRecordingRealStarted:",timeTillRecordingRealStarted)
        print("TimeDistance:", timeDistance)
        print("TimeUntilSoundPlayed:", timeUntilSoundPlayed)
        print("TimeRec:", timeRec)
        print("Relative Time:", relativeTime)
        print("Distance:", distance)

    return distance


getDistanceToSpeaker(stream, CHUNK, realChunk, frequencyPlay, timePlaying, True, 330, 0.04)