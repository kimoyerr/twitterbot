#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script for TwitterBot"""

# Generic/Built-in
import argparse
from os import environ

# Other Libs
import tweepy
import pymongo

__author__ = "Krishna Yerramsetty"
__copyright__ = ""
__credits__ = ["https://dev.to/emcain/how-to-set-up-a-twitter-bot-with-python-and-heroku-1n39", "https://fedoramagazine.org/learn-build-twitter-bot-python/"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Krishna Yerramsetty"
__email__ = "kimoyerr@gmail.com"
__status__ = "Dev"


# Get the access keys and tokens from the Heroku environment
API_KEY = environ['API_KEY']
API_SECRET_KEY = environ['API_SECRET_KEY']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']


# This is the meat of the script that drives the twitterbot
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


# MongoDB atlas connection
mongo_client = pymongo.MongoClient(environ['MONGODB_ATLAS_CONNECTION'])
tweets_db = mongo_client.tweets
crispr_collections = tweets_db.crispr_tweets


class MyStreamListener(tweepy.StreamListener):
    """"Listens to tweets and inserts each tweet into a MongoDB collection"""

    def on_status(self, status):
        """When raw data is received from Twitter server, it is inserted into the MongoDB collection

        Args:
          status: Raw data from Twitter server
        """

        id_str = status.id_str
        created = status.created_at
        text = status.text
        fav = status.favorite_count
        name = status.user.screen_name
        description = status.user.description
        loc = status.user.location
        user_created = status.user.created_at

        # Load the data to MongoDB if its not a retweet
        if not 'RT @' in status.text:
            # print(status.text)
            crispr_collections.insert_one({
                "_id": id_str,
                "tweet_text": text,
                "tweet_created": created,
                "tweet_loc": loc,
                "user_name": name
            })

    def on_error(self, status_code):
        """When error status code is received from Twitter server

        Args:
            status_code: Error code from Tiwtter
        Returns:
            False: If status code is 420 (when app is rate limited by twitter server)
            Nothing: All other status codes
        """

        print('error')
        if status_code == 420:
            print('encountered error')
            #returning False in on_data disconnects the stream
            return False


if __name__ == '__main__':
    """Main part of the code where the streamlistener is created and run"""

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(track=['crispr'], async=True)

