import json
from pymongo import Connection
import tweepy

conn = Connection().rally
database = conn.trump

consumer_key = 'rzWMCh6HfUUF1dibWaHTQzbYt'
consumer_secret = 'umR7F5azzryDtXc1nvmKPMd87S9u9FN8SxkZJtodoQgshGQt8Y'
access_token = '338457897-iWdj6trnSDHnV8sBIjrfaiTSRM0XsmutFCurdXMF'
access_token_secret = 'hzhtetCHikSwsSHhkX8yg5dhZb5eOQZpoAMdvKbN4dHin'

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        try:
                print "found tweet"
                # Twitter returns data in JSON format - we need to decode it first
                decoded = json.loads(data)
                if 'coordinates' in decoded:
                        if decoded['coordinates']:
                                print "inserting"
                                database.insert(decoded)

        except ValueError, KeyError:
                print "error"
                pass

    def on_error(self, status):
        print status
 
if __name__ == '__main__':
        l = StdOutListener()
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        locs = [-83.623402,32.838509,-83.613832,32.845828]
        stream = tweepy.Stream(auth,l)
        stream.filter(locations=locs,async=False)