#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import sys
import urllib
import os
from google.cloud import videointelligence

#Twitter API credentials
consumer_key = "Zn2pUf47yCpQctv9yknmeaRk0"
consumer_secret = "Zluvj7qJ1b4QpcPFa8Y5rFhTDv4wDbfRuSkCbzKPMig2pKp50m"
access_key = "958121468163973120-zTs2rmOABdByQ7G7VWvpZeRXcRvdkaz"
access_secret = "8FeVaMtf8FSEZVuv3EOK53cRKHek4OyK4tpSOzZvVVjrR"


def get_all_tweets(screen_name):
        #Twitter only allows access to a users most recent 3240 tweets with this method

        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)

        #initialize a list to hold all the tweepy Tweets
        alltweets = []

        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = screen_name,count=1)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
                print "getting tweets before %s" % (oldest)

                #all subsequent requests use the max_id param to prevent duplicates
                new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

                #save most recent tweets
                alltweets.extend(new_tweets)

                #update the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1

                print "...%s tweets downloaded so far" % (len(alltweets))

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
                urllib.urlretrieve(outtweets[i][0],"image_%s.jpg" % a)
                int(a)
                a = a + 1

        os.system('ffmpeg -r 1 -i image_%001d.jpg -vcodec libx264 -b:v 2M -maxrate 2M -bufsize 1M -y -an -filter:v "setpts=2.0*PTS" -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" video.mp4')


if __name__ == '__main__':
        #pass in the username of the account you want to download
        get_all_tweets("TerrierTennis")