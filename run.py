# python code goes here
import os
import tweepy as tw
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
search_words = input("Add your keyword here: \n")
date_since = input("Add your date range here: \n")
language_search = input("Add your prefered language here: \n")

new_search = search_words + "-filter:retweets"

# Collect tweets
tweets = tw.Cursor(
              api.search,
              q=new_search,
              lang=language_search,
              since=date_since
                  ).items(20)

tweets

# Iterate and print tweets
for tweet in tweets:
    print(tweet.text, end='\n\n')
