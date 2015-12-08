#from django.core.management.base import NoArgsCommand, BaseCommand, CommandError from django.contrib.gis.geos import Point from django.db.models import F from 
#locations import *
import sys
import time
from datetime import datetime
#import pytz
import json
import tweepy
import tweepy.streaming
from tweepy import OAuthHandler
#import linear as classifier
from pymongo import Connection
import cPickle as pickle
from Oauth import main as GetAPI
import re
import string
from geo_utils import distance_from_rally,bounding_box_centroid

candidate = "MNF"
party = ''
rally_id = 2
locs = [-81.703413,41.501587,-81.690924,41.509557]

class StdOutListener(tweepy.StreamListener):
	def on_data(self, status):
		status = json.loads(status)
		if status['lang'] and status['lang'] != "en":
			#print "non english"
			pass
		if not(status['geo'] or status['coordinates'] or status['place']):
			print "no geo"
			pass
		if not(status['coordinates']) and status['place']:
			try:
				coordinates = bounding_box_centroid(status['place']['bounding_box']['coordinates'])
			except Exception:
				print "place problem"
				pass
		else:
			coordinates = status['coordinates']
		if len(coordinates) != 2:
			print 'bad coords',len(coordinates)
			pass
			
		try:
			dist = distance_from_rally(coordinates,locs)
		except KeyError:
			print "key error"
			dist = 0
		print coordinates," ",dist,' mi'
		print status['text']
		print

		tweet = {
			'id_str' : status['id_str'],
			'created_at' : status['created_at'],
			'date_time' : datetime.now().__str__(),
			'lang' : status['lang'],
			'text' : status['text'],
			'entities' : json.dumps(status['entities']),
			'user_id_str' : status['user']['id_str'],
			'user_name' : status['user']['name'],
			'user_screen_name' : status['user']['screen_name'],
			'user_profile_image_url' : status['user']['profile_image_url'],
			"candidate" : candidate,
			"party" : party,
			"rally_id" : rally_id,
			"dist" : dist
		}
		if status['geo']:
			tweet["geo"] = status['geo']
		if status['coordinates']:
			tweet["coordinates"] = status['coordinates']
		if status['place'] and status['place']['bounding_box'] and status['place']['bounding_box']['coordinates'] and status['place']['url'] and status['place']['name'] and status['place']['id']:
			place = status['place']
			tweet["place"] = {
				"id" : place['id'],
				"name" : place['full_name'],
				"url" : place['url'],
				"coordinates" : place['bounding_box']['coordinates']
			}
		database.insert(tweet)

if __name__ == '__main__':

	
	conn = Connection().rally
	database = conn.nflLocal
	
	consumer_key = '44WIYaybMnBNdWXV9uHEJukle'
	consumer_secret = '12m8ZijW8ZRwH31pqtBt9RE7GmyUvX2S2OLipITmOXcZxhz6ju'
	access_token = '4332606617-lRhvQ02KhIOpwcgTC1BECJUdcMNiydMXTB9UtkZ'
	access_token_secret = 'pFmQeTHZOfpRhyNcJM5yzOtA5VkMj1n95BSFzvhVm9Ayk'
		
	l = StdOutListener()
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	

	
	stream = tweepy.Stream(auth,l)
	stream.filter(locations=locs,async=False)