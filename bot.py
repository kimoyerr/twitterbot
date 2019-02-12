#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script for TwitterBot"""

# Generic/Built-in
import argparse
from os import environ

# Other Libs
import tweepy

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
public_tweets = api.home_timeline()

for tweet in public_tweets:
    print(tweet.text)

