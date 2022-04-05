#importing all dependencies
import dotenv
import numpy as np
import tweepy
import os
from dotenv import load_dotenv
#variables for accessing twitter API
load_dotenv()

consumer_key = os.getenv('consumer_key')
consumer_secret_key = os.getenv('consumer_secret_key')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

def TweetText(_message):

    #authenticating to access the twitter API
    auth=tweepy.OAuthHandler(consumer_key,consumer_secret_key)
    auth.set_access_token(access_token,access_token_secret)
    api=tweepy.API(auth)
    
    # send tweet
    api.update_status(_message)

#TweetText("This is now in stock\nhttps://www.amazon.com/dp/B07WVN6CWT?tag=amazondn01-20")