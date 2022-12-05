import pyaudio, time, progressbar, pysine, wave
from threading import Thread
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft


class AudioListener: 

    delay = 2
    frequency = 10000
    timePlaying = 2
    velocity = 343 


    #AUDIO INPUT
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100 # 44100
    CHUNK = 1024 * 176 # RATE * (timeRecording + delay)
    REALCHUNK = int(1024 / 2)
    timeSoundPlayedAt = -1

    windowSize = 1 / RATE # time between each frame

    audio = pyaudio.PyAudio()

    def writeToFile(self, fileName, chunk): 
        wf = wave.open(fileName, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(chunk)
        wf.close()




    STREAM = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK, input_device_index=1)


    def threadPlaySound(self, freqsss, timePlay):
        global timeSoundPlayedAt
        time.sleep(self.delay)
        timeSoundPlayedAt = time.time_ns()
        pysine.sine(frequency=freqsss, duration=timePlay)
        print("Sound Played")

    def getDistanceToSpeaker(self, FREQUENCYPLAY, TIMEPLAYING, DEBUG, VELOCITY, THRESHHOLD): # Function to calculate Distance from Speaker and Microphone
        frequencyPlayed = int((FREQUENCYPLAY - (FREQUENCYPLAY % (self.RATE / self.REALCHUNK))))
        indexOfFrequency = int((FREQUENCYPLAY - (FREQUENCYPLAY % (self.RATE / self.REALCHUNK))) / (self.RATE/self.REALCHUNK)) # Calculating index of frequency we want to listen to
        
        threadPlayer = Thread(target=self.threadPlaySound, args=((frequencyPlayed, TIMEPLAYING)))
        threadPlayer.start()

        print("Start recording")
        timeRecordingStart = time.time_ns() # Messuring recording time
        hugeChunk = self.STREAM.read(self.CHUNK)
        timeRecordingEnd = time.time_ns()
        print("End recording")

        timeTillRecordingRealStarted = ((timeRecordingEnd - timeRecordingStart) * 1e-9) - (self.CHUNK / self.RATE)

        frameFoundAt = 0

        bar = progressbar.ProgressBar(max_value=self.CHUNK)
        
        readData = np.frombuffer(hugeChunk, dtype='h')  # Converting Chunk to readable Chunk
        readData = np.array(readData, dtype='h')/140 + 255
        vals = []

        indexOfFrequency = int((frequencyPlayed - (frequencyPlayed % (self.RATE / self.REALCHUNK))) / (self.RATE/self.REALCHUNK)) # Calculating index of frequency we want to listen to

        frameFoundAt = -1
        arr = []

        for i in range(0, self.CHUNK - self.REALCHUNK): # Checking through all sub-chunks, detects first 
            bar.update(i)
            chunk = readData[i:i+self.REALCHUNK*2]
            realValues = np.abs(fft(chunk)[0:self.REALCHUNK]) * 2 / (128 * self.REALCHUNK)
            valueOfFrequency = realValues[indexOfFrequency]
            arr.append(realValues[indexOfFrequency])

            if (valueOfFrequency > THRESHHOLD and frameFoundAt == -1):
                frameFoundAt = i

        
        fig, (ax1) = plt.subplots(1, figsize=(15, 7))
        fig.show() 
        ax1.plot(np.arange(0, len(arr), 1), np.array(arr), color='g', linestyle='-', lw=2)
        ax1.plot(frameFoundAt, arr[frameFoundAt], color='r', linestyle=':')
        fig.show()
        #fig.waitforbuttonpress()
        ax1.set_title("Values for frequency")

        timeDistance = ((frameFoundAt / self.RATE) + timeTillRecordingRealStarted) * 1e+9 # Time (relative) we heard the sound at (correction for delay in the STREAM.READ() methode) (ns)
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
