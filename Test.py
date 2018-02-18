#!/usr/bin/env python
# encoding: utf-8

import twitter
import os
import time

#Cleans folder from files generated in previous runs
#for file in os.listdir():
 #   if file.endswith('.jpg'):
  #      os.remove(file)
    #elif file.endswith('.mp4'):
     #   os.remove(file)

#Create variables to store time and folder size before program run
size_before = sum(os.path.getsize(f) for f in os.listdir('.') if os.path.isfile(f))
time_before = time.time()

#Test 1: valid program run. 
twitter.get_all_tweets("TerrierTennis")

#variables that stores size and time after a valid run of the program is performed
size_after = sum(os.path.getsize(f) for f in os.listdir('.') if os.path.isfile(f))
time_after = time.time()

#variable that represent the overall runtime of the program 
run_time = time_after-time_before
size = size_after-size_before
print('Valid program run took ', run_time , ' seconds to run and ',size, 'bytes of memory')

#Test 2: Invalid twitter username, program breaks and error message from tweepy API shows
twitter.get_all_tweets("gvjhabv0845ythfnv")

#Test 3: when input is twitter with no images on feed, program breaks with error message of out of range
twitter.get_all_tweets("danaszapirog")
