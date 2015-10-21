from TwitterAPI import TwitterAPI
import config

class Twitter:

    def __init__(self):

        configuration = config.config()
        self.access_token_key = configuration['access_token']
        self.access_token_secret = configuration['access_token_secret']
        self.consumer_key = configuration['consumer_key']
        self.consumer_secret = configuration['consumer_key_secret']
        self.initiate_connection()

    def initiate_connection(self):
        self.api = TwitterAPI(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret)

    def stream_location(self):
        r = self.api.request('statuses/filter', {'locations':'-74,40,-73,41'})
        for item in r:
            print(item)

