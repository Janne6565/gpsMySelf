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
                frames_per_buffer=CHUNK, input_device_index=1)

def getVals(freqs): 
    inputt = stream.read(CHUNK) 
    freqs, results = goertzel.goertzel(inputt, RATE, (freqs[0], freqs[1]))
    return freqs, results

if __name__ == "__main__": 
    microphoneFactor = 100000000 # Microphone mutliplys Volume
    sensitivity = 10
    print("Running The code")
    while True:
        freqs, results = getVals((800, 800))
        res = np.array(results)[:,2]
        realResult = res / microphoneFactor
        if (realResult >= sensitivity):
            print("Called")

