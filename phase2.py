import tweepy #https://github.com/tweepy/tweepy
import csv
import sys
import urllib
import argparse
import io
import os
from pymongo import MongoClient
from google.cloud import videointelligence

import argparse

from google.cloud import videointelligence


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/Satyajit/EC500/Twitter_Project/google.json"
consumer_key = "Zn2pUf47yCpQctv9yknmeaRk0"
consumer_secret = "Zluvj7qJ1b4QpcPFa8Y5rFhTDv4wDbfRuSkCbzKPMig2pKp50m"
access_key = "958121468163973120-zTs2rmOABdByQ7G7VWvpZeRXcRvdkaz"
access_secret = "8FeVaMtf8FSEZVuv3EOK53cRKHek4OyK4tpSOzZvVVjrR"

def get_tweets(handle, amount):
	#authorize twitter, initialize tweepy
	try:
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_key, access_secret)
		api = tweepy.API(auth)
	except tweepy.TweepError:
		print("The keys and secrets are invalid")

	alltweets = []

	new_tweets = api.user_timeline(screen_name = handle,count=1)

	alltweets.extend(new_tweets)

	oldest = alltweets[-1].id - 1

	while len(new_tweets) > 0:
	        new_tweets = api.user_timeline(screen_name = handle,count=amount,max_id=oldest)
	        alltweets.extend(new_tweets)
	        oldest = alltweets[-1].id - 1

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
	                outtweets.append([tweet.entities['media'][0]['media_url']])

	return outtweets	      


def download_images(outtweets, amount):
	a = 0
	for i in range(0,int(amount)):
		str(a)
        urllib.urlretrieve(outtweets[i][0],"image_%s.jpg" % a)
        int(a)
        a = a + 1

def create_video():
	try:
		os.system('ffmpeg -r 1 -i image_%001d.jpg -vcodec libx264 -b:v 2M -maxrate 2M -bufsize 1M -y -an -filter:v "setpts=2.0*PTS" -vf "scale=w=1280:h=720:force_original_aspect_ratio=1,pad=1280:720:(ow-iw)/2:(oh-ih)/2" video.mp4')
	except:
		print("could not create video")

def analysis():

	labels = dict()
	labels['VideoLabel'] = []
	labels['CategoryLabel'] = []
	
	video_client = videointelligence.VideoIntelligenceServiceClient()
	features = [videointelligence.enums.Feature.LABEL_DETECTION]


	with io.open('video.mp4', 'rb') as movie:
		input_content = movie.read()

	operation = video_client.annotate_video(features=features, input_content=input_content)

	result = operation.result(timeout=90)

	segment_labels = result.annotation_results[0].segment_label_annotations

	for i, segment_label in enumerate(segment_labels):
		labels['VideoLabel'].append(segment_label.entity.description)
		for category_entity in segment_label.category_entities:
			labels['CategoryLabel'].append(category_entity.description)

	return labels

def Initialize():
	try: 
		client = MongoClient('localhost:27017')
		db = client.TwitterData
	except Exception,e:
		print(e)

def Insert(data):
	client = MongoClient('localhost:27017')
	db = client.TwitterData
	db.TwitterData.insert_one(data)

def main():
	handle = raw_input("Enter the twitter handle you wish to receive from: ")
	amount = raw_input("Enter the amount of images you wish to receive: ")
	outtweets = get_tweets(handle, amount)
	download_images(outtweets,amount)
	create_video()
	labels = analysis()
	data = {
		"twitter_handle": handle,
		"num_of_images": amount, 
		"labels":labels
	}
	Initialize()
	Insert(data)

main()














