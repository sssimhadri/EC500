import tweepy #https://github.com/tweepy/tweepy
import csv
import sys
import urllib
import argparse
import io
import os
import subprocess
from google.cloud import videointelligence

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/Satyajit/EC500/Twitter_Project/google.json"

#Twitter API credentials
'''
consumer_key = "Zn2pUf47yCpQctv9yknmeaRk0"
consumer_secret = "Zluvj7qJ1b4QpcPFa8Y5rFhTDv4wDbfRuSkCbzKPMig2pKp50m"
access_key = "958121468163973120-zTs2rmOABdByQ7G7VWvpZeRXcRvdkaz"
access_secret = "8FeVaMtf8FSEZVuv3EOK53cRKHek4OyK4tpSOzZvVVjrR"
'''

print("Hello, this is what this program does\n 1. Input a twitter handle\n 2. Returns a video of the amount of tweets you want\n 3. Analyzes the images with Google API")
consumer_key = raw_input("Enter in the consumer key: ")
consumer_secret = raw_input("Enter in the consumer secret: ")
access_key = raw_input("Enter in the access key: ")
access_secret = raw_input("Enter in the access secret: ")

#authorize twitter, initialize tweepy
try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
except tweepy.TweepError:
        print("The keys and secrets are invalid")


handle = raw_input("Please enter in the twitter handle: ")
amount = raw_input("Enter the amount of tweets you want to get(200 is the maximum): ")

#initial list to hold all tweepy Tweets
alltweets = []

#request for most recent tweets
new_tweets = api.user_timeline(screen_name = handle,count=1)

#save most recent tweets
alltweets.extend(new_tweets)

#save id for the oldest tweet minus one
oldest = alltweets[-1].id - 1

while len(new_tweets) > 0:
        print("getting tweets....")

        #all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = handle,count=amount,max_id=oldest)

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

video_amount = raw_input("Enter the amount of images you want in your video: ")

a = 0

for i in range(0,int(video_amount)):
        str(a)
        urllib.urlretrieve(outtweets[i][0],"image_%s.jpg" % a)
        int(a)
        a = a + 1

os.system('ffmpeg -r 1 -i image_%001d.jpg -vcodec libx264 -b:v 2M -maxrate 2M -bufsize 1M -y -an -filter:v "setpts=2.0*PTS" -vf "scale=w=1280:h=720:force_original_aspect_ratio=1,pad=1280:720:(ow-iw)/2:(oh-ih)/2" video.mp4')

path = raw_input("Enter in the path to your video file: ")

"""Detect labels given a file path."""
video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.LABEL_DETECTION]

with io.open(path, 'rb') as movie:
    input_content = movie.read()

operation = video_client.annotate_video(
    features=features, input_content=input_content)
print('\nProcessing video for label annotations:')

result = operation.result(timeout=90)
print('\nFinished processing.')

# Process video/segment level label annotations
segment_labels = result.annotation_results[0].segment_label_annotations
for i, segment_label in enumerate(segment_labels):
    print('Video label description: {}'.format(
        segment_label.entity.description))
    for category_entity in segment_label.category_entities:
        print('\tLabel category description: {}'.format(
            category_entity.description))

    for i, segment in enumerate(segment_label.segments):
        start_time = (segment.segment.start_time_offset.seconds +
                      segment.segment.start_time_offset.nanos / 1e9)
        end_time = (segment.segment.end_time_offset.seconds +
                    segment.segment.end_time_offset.nanos / 1e9)
        positions = '{}s to {}s'.format(start_time, end_time)
        confidence = segment.confidence
        print('\tSegment {}: {}'.format(i, positions))
        print('\tConfidence: {}'.format(confidence))
    print('\n')

# Process shot level label annotations
shot_labels = result.annotation_results[0].shot_label_annotations
for i, shot_label in enumerate(shot_labels):
    print('Shot label description: {}'.format(
        shot_label.entity.description))
    for category_entity in shot_label.category_entities:
        print('\tLabel category description: {}'.format(
            category_entity.description))

    for i, shot in enumerate(shot_label.segments):
        start_time = (shot.segment.start_time_offset.seconds +
                      shot.segment.start_time_offset.nanos / 1e9)
        end_time = (shot.segment.end_time_offset.seconds +
                    shot.segment.end_time_offset.nanos / 1e9)
        positions = '{}s to {}s'.format(start_time, end_time)
        confidence = shot.confidence
        print('\tSegment {}: {}'.format(i, positions))
        print('\tConfidence: {}'.format(confidence))
    print('\n')

# Process frame level label annotations
frame_labels = result.annotation_results[0].frame_label_annotations
for i, frame_label in enumerate(frame_labels):
    print('Frame label description: {}'.format(
        frame_label.entity.description))
    for category_entity in frame_label.category_entities:
        print('\tLabel category description: {}'.format(
            category_entity.description))

    # Each frame_label_annotation has many frames,
    # here we print information only about the first frame.
    frame = frame_label.frames[0]
    time_offset = frame.time_offset.seconds + frame.time_offset.nanos / 1e9
    print('\tFirst frame time offset: {}s'.format(time_offset))
    print('\tFirst frame confidence: {}'.format(frame.confidence))
    print('\n')





























