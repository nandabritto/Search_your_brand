# python code goes here
import os
import tweepy as tw
import pandas as pd 

from dotenv import load_dotenv

load_dotenv()

consumer_key = os.environ.get('API_KEY')
consumer_secret= os.environ.get('API_SECRET_KEY')
access_token= os.environ.get('ACCESS_TOKEN')
access_token_secret= os.environ.get('ACCESS_TOKEN_SECRET')

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


api.update_status("Look, I'm tweeting from #Python in my #earthanalytics class! @EarthLabCU")