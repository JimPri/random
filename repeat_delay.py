# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 17:55:47 2016

Play back recorded sound with a slight delay.
"""

import pyaudio

CHUNK = 441
WIDTH = 2
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
LIMIT = 2000


MIN_TIME = 0.2
MAX_TIME = 1

import threading
import time

lock = threading.Lock()
samples = []
flag = False

def record():
    global samples
    global lock
    
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                frames_per_buffer=CHUNK)

    while not flag:
        data = stream.read(CHUNK)
        
        lock.acquire()
        
        samples.append((time.time(), data))
    
        lock.release()
    
def playback():
    global samples
    global lock
    global flag
    
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=False,
                output=True,
                frames_per_buffer=CHUNK)
               
    count = 0
    while not flag:
        lock.acquire()
        
        if len(samples):
            
            ts, data = samples[0]
            
            delay = time.time() - ts
            
            if delay < MIN_TIME:
                lock.release()
                continue
            
            samples = samples[1:]
            
            if delay > MAX_TIME:
                print("DELAY", delay)
                lock.release()
                continue
            
            lock.release()
            
            print(count, len(samples), time.time() - ts)
            
            stream.write(data, CHUNK)
            count = count + 1
            flag = count == LIMIT
            
            continue
    
        lock.release()

record_thread = threading.Thread(None, record)
playback_thread = threading.Thread(None, playback)

record_thread.start()
playback_thread.start()

record_thread.join()
playback_thread.join()
