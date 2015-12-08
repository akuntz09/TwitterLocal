import json
from pymongo import Connection
import tweepy

conn = Connection().rally
database = conn.nflGlobal

consumer_key = '9j6i1ooWksneZTx4OWa4rJKjc'
consumer_secret = 'U2NDGvtidQBXQjNzdeqtxjuPgvoeJ1g9GhBvwF9wFvCGKpy1PV'
access_token = '2185695936-dApTkWzzX4picNKAmonuagmw8OkKT64iKykWJzZ'
access_token_secret = 'vy96AaHgL5TeT7CnQBeoroORshvNzNWIQpg24jEvUUY8I'

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
		
		terms = ['#MNF', '#BALvsCLE','#CLEvsBAL','#MondayNightFootball']
		stream = tweepy.Stream(auth,l)
		stream.filter(track=terms,async=False)