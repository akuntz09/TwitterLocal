import json
from pymongo import Connection
import tweepy

conn = Connection().rally
database = conn.trumpGlobal3

consumer_key = 'SCjGeQgk6VwgpXMXwv0nw3bnH'
consumer_secret = 'GWRLBQRCyZUGj11dfApQsXyNO1xUAtxdWk3jJgAfnXhcuCHVCa'
access_token = '1180007930-KEu8TqyPmSa4HC1BFcGxhJcsDwbfjYpWEWTyfSE'
access_token_secret = 'wRhMtww15B6RjKGj6eK8UjwRUM83N63ZCFKqWTl4SwhEL'

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
	def on_data(self, data):
		try:
				# Twitter returns data in JSON format - we need to decode it first
				decoded = json.loads(data)
				database.insert(decoded)
				print decoded['text']
	
		except ValueError, KeyError:
				print "error"
				pass

	def on_error(self, status):
		print status
 
if __name__ == '__main__':
		l = StdOutListener()
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		
		terms = ['#donaldtrump','#trump','#makeamericagreatagain','#trumptrain','#trump2016']
		stream = tweepy.Stream(auth,l)
		stream.filter(track=terms,async=False)