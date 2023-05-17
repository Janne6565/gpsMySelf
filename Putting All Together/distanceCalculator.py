import pyaudio, time, progressbar, pysine, wave
from threading import Thread
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft


class AudioListener: 
    
    delay = 2
    frequency = 30000
    timePlaying = 2
    velocity = 343


    #AUDIO INPUT
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100 # 44100
    REALCHUNK = int(1024 / 2)
    timeSoundPlayedAt = -1
    windowSize = 1 / RATE # time between each frame


    def writeToFile(self, fileName, chunk): 
        wf = wave.open(fileName, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(chunk)
        wf.close()


    def threadPlaySound(self, freqsss, timePlay):
        global timeSoundPlayedAt
        print("Frequency playing: " + str(freqsss))
        time.sleep(self.delay)
        timeSoundPlayedAt = time.time_ns()
        pysine.sine(frequency=freqsss, duration=timePlay)
        print("Sound Played")

    def getDistanceToSpeaker(self, FREQUENCYPLAY, TIMEPLAYING, DEBUG, VELOCITY, THRESHHOLD): # Function to calculate Distance from Speaker and Microphone

        chunk = (TIMEPLAYING + self.delay) * self.RATE

        frequencyPlayed = int((FREQUENCYPLAY - (FREQUENCYPLAY % (self.RATE / self.REALCHUNK))))
        indexOfFrequency = int((FREQUENCYPLAY - (FREQUENCYPLAY % (self.RATE / self.REALCHUNK))) / (self.RATE/self.REALCHUNK)) # Calculating index of frequency we want to listen to

        audio = pyaudio.PyAudio()
        STREAM = audio.open(format=self.FORMAT, channels=self.CHANNELS,
                    rate=self.RATE, input=True,
                    frames_per_buffer=chunk, input_device_index=1)
        
        threadPlayer = Thread(target=self.threadPlaySound, args=((frequencyPlayed, TIMEPLAYING)))
        threadPlayer.start()

        print("Start recording")
        timeRecordingStart = time.time_ns() # Messuring recording time
        hugeChunk = STREAM.read(chunk)
        self.writeToFile("test.wav", hugeChunk)
        timeRecordingEnd = time.time_ns()
        print("Chunk Size:", chunk)
        print("Estimated time for Chunk:", TIMEPLAYING + self.delay)
        print("Time it took to listen to microphone:", (timeRecordingEnd - timeRecordingStart) * 1e-9)
        print("End recording")

        timeTillRecordingRealStarted = ((timeRecordingEnd - timeRecordingStart) * 1e-9) - ((TIMEPLAYING + self.delay))

        frameFoundAt = 0

        bar = progressbar.ProgressBar(max_value=chunk)
        
        readData = np.frombuffer(hugeChunk, dtype='h')  # Converting Chunk to readable Chunk
        readData = np.array(readData, dtype='h')/140 + 255

        indexOfFrequency = int((frequencyPlayed - (frequencyPlayed % (self.RATE / self.REALCHUNK))) / (self.RATE/self.REALCHUNK)) # Calculating index of frequency we want to listen to

        frameFoundAt = -1
        arr = []

        for i in range(0, (chunk) - self.REALCHUNK * 2): # Checking through all sub-chunks, detects first 
            bar.update(i)
            chunk = readData[i:i+self.REALCHUNK*2]
            realValues = np.abs(fft(chunk)[0:self.REALCHUNK]) * 2 / (128 * self.REALCHUNK)
            valueOfFrequency = realValues[indexOfFrequency]
            arr.append(realValues[indexOfFrequency])

            if (valueOfFrequency > THRESHHOLD and frameFoundAt == -1):
                frameFoundAt = i

        
        fig, (ax1) = plt.subplots(1, figsize=(15, 7))
        ax1.plot(np.arange(0, len(arr), 1), np.array(arr), color='g', linestyle='-', lw=2)
        
        ax1.set_title("Values for frequency")

        timeDistance = ((frameFoundAt / self.RATE) + timeTillRecordingRealStarted) * 1e+9 # Time (relative) we heard the sound at (correction for delay in the STREAM.READ() methode) (ns)
        timeUntilSoundPlayed = timeSoundPlayedAt - timeRecordingStart # Time (relative) we heard the sound at (ns)
        timeRec = timeDistance - timeUntilSoundPlayed # Time (relative) it took the sound to travel to the microphone (ns)
        relativeTime = timeRec * 1e-9 # Time (relative) it took the sound to travel to the microphone (s)
        distance = relativeTime * VELOCITY # Distance calculated by the time the sound traveled 

        frameItShouldBeOn = (timeSoundPlayedAt - timeRecordingStart) / self.RATE 
        frameItIsOn = frameFoundAt

        if (DEBUG): 
            print("Max value:", max(arr))
            print("Found on:", frameFoundAt)
            print("TimeTillRecordingRealStarted:", timeTillRecordingRealStarted)
            print("TimeDistance:", timeDistance)
            print("TimeUntilSoundPlayed:", timeUntilSoundPlayed)
            print("TimeRec:", timeRec)
            print("Relative Time:", relativeTime)
            print("Distance:", distance)

            print("For Distance = 0: Error of ", frameItShouldBeOn - frameItIsOn, " Frames")
            print("This is equal to ", (frameItShouldBeOn - frameItIsOn) / self.RATE, " Seconds")
            print("Time we take: ", self.delay * self.RATE)

        fig.show()
        fig.waitforbuttonpress()
        return distance


if (__name__ == "__main__"):
    audio = AudioListener()
    #audio.threadPlaySound(10000, 10)
    arr = []

    a1 = audio.getDistanceToSpeaker(10000, 2, True, 343, 0.003)
    # a2 = audio.getDistanceToSpeaker(10000, 2, False, 343, 0.00036)
    # print([a1, a2])