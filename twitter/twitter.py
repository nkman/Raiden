from TwitterAPI import TwitterAPI
import rethinkdb as r
from db import database
import config

class Twitter:

    def __init__(self):

        configuration = config.twitter_credentials()
        self.access_token_key = configuration['access_token']
        self.access_token_secret = configuration['access_token_secret']
        self.consumer_key = configuration['consumer_key']
        self.consumer_secret = configuration['consumer_key_secret']

        self.db = database.Database()
        self.connection = self.db.connection_var()

        self.create_table()
        self.initiate_connection()

    def create_table(self):
        try:
            r.db('raiden').table_create('twitter').run(self.connection)
            print 'Created table [raiden.twitter]'
        except Exception, e:
            print 'Error occured during twitter table creation! Maybe it already exists!'
            print str(e)
        
    def initiate_connection(self):
        self.api = TwitterAPI(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret)

    def stream_location(self):
        #bbox = left,bottom,right,top
        #bbox = min Longitude , min Latitude , max Longitude , max Latitude 
        req = self.api.request('statuses/filter', {'locations':'70.02, 7.80, 91.58, 35.67'})
        #req = self.api.request('statuses/filter', {'locations':'77.1475, 28.5943, 77.3218, 28.6843'}) Delhi
        count = 0
        for item in req:
            r.db('raiden').table("twitter").insert(item).run(self.connection)
            count += 1
            print count

