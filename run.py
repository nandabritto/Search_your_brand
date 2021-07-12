# python code goes here
import os
import tweepy as tw
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import pandas as pd


from dotenv import load_dotenv

load_dotenv()

consumer_key = os.environ.get('API_KEY')
consumer_secret = os.environ.get('API_SECRET_KEY')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

"""
Code based on earthdatascience.org
"""
# Define the search term and the date_since date as input
def search_tweet():
    search_words = input("Add your keyword here: \n")
    language_search = input("Add your prefered language here: \n")
    new_search = search_words + "-filter:retweets"

    tweets = tw.Cursor(
                  api.search,
                  q=new_search,
                  count=5,
                  lang=language_search,
                  tweet_mode='extended')

    maxCount = 5
    count = 0
    for tweet in tweets.items():    
        print()
        print("Tweet Information")
        print("================================")
        print("Text: ", tweet.full_text)
        print()

        count = count + 1
        if count == maxCount:
            break

search_tweet()