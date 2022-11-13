import pyaudio, goertzel, time
import numpy as np
import matplotlib.pyplot as plt

#AUDIO INPUT
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

audio = pyaudio.PyAudio()



def getAllSoundInputs():
    info = audio.get_host_api_info_by_index(0)
    numDevices = info.get("deviceCount")

    for i in range(numDevices): 
        if (audio.get_device_info_by_host_api_device_index(0, i).get("maxInputChannels") > 0): 
            print("Input device ID: ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get("name"))

stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK, input_device_index=1)

def getVals(freqss):  # freqs = (796, 797)
    inputt = stream.read(CHUNK)
    return calculateFromChunk(input, freqss)

def calculateFromChunk(chunk, freqs): 
    freqss, results = goertzel.goertzel(chunk, RATE, freqs)
    return freqss, results


def getValueFromVal(res, microphoneFactor): 
    return res[:,2] / microphoneFactor
