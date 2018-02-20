#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import sys
import urllib
import os
import subprocess
import json
import requests
import io
import re
import glob
from urllib.request import urlretrieve

from google.cloud import vision
from google.cloud.vision import types
from os import listdir


#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def get_all_tweets(screen_name):
        #Twitter only allows access to a users most recent 3240 tweets with this method

        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)

            # verifys credentials
        valid_credentials = api.verify_credentials()
        if (valid_credentials == False):
            print ('Incorrect credentials')
            return 
        #initialize a list to hold all the tweepy Tweets
        alltweets = []

        #make initial request for most recent tweets (200 is the maximum allowed count)
        try:
            new_tweets = api.user_timeline(screen_name = screen_name,count=1)
            
        except tweepy.TweepError as e:
            print('ERROR: could not download tweeter feed. \nException description:')
            print(e)
            return     
        #save most recent tweets
        alltweets.extend(new_tweets)

        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
                #print "getting tweets before %s" % (oldest)

                #all subsequent requests use the max_id param to prevent duplicates
                new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

                #save most recent tweets
                alltweets.extend(new_tweets)

                #update the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1

                #print "...%s tweets downloaded so far" % (len(alltweets))

        #go through all found tweets and remove the ones with no images 
        outtweets = [] #initialize master list to hold our ready tweets
        for tweet in alltweets:
                #not all tweets will have media url, so lets skip them
                try:
                        tweet.entities['media'][0]['media_url']
                except (NameError, KeyError):
                        #we dont want to have any entries without the media_url so lets do nothing
                        pass
                else:
                        #got media_url - means add it to the output
                        outtweets.append([ tweet.entities['media'][0]['media_url']])


        print("--------------------- LINKS START FROM HERE ---------------------")


        a = 0

        for i in range(0,20):
                str(a)
                urllib.request.urlretrieve(outtweets[i][0],"image_%s.jpg" % a)
                int(a)
                a = a + 1
                
        try:
            os.system('ffmpeg -r 1 -i image_%001d.jpg -vcodec libx264 -b:v 2M -maxrate 2M -bufsize 1M -y -an -filter:v "setpts=2.0*PTS" -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" video.mp4')
        except (RuntimeError, TypeError, NameError):
            print('ERROR: ffmpeg unable to to create video')
            pass

        # creates google vision API client
        client = vision.ImageAnnotatorClient()

        # creates ouput file to write lables
        file = open("./imagelabels.txt", "w")

        # for loop to go through .jpg pictures in output folder
        pictures = [pic for pic in listdir(".") if pic.endswith('jpg')]
        for picture in pictures:
            file_name = os.path.join(os.path.dirname(__file__), picture)

            # Loads the image into memory
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()

                image = types.Image(content=content)

                # Performs label detection on the image file
                response = client.label_detection(image=image)
                labels = response.label_annotations

                # writes current image  URL
                file.write('Lables for  ' + picture + ' :\n')
                print('Lables:' + picture)

                for label in labels:
                    # writes current image labels
                    file.write(label.description + '\n')
                    print(label.description)

if __name__ == '__main__':
        #pass in the username of the account you want to download
        get_all_tweets("")
