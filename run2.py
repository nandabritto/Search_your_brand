import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

# personal details
consumer_key = os.environ.get('API_KEY')
consumer_secret = os.environ.get('API_SECRET_KEY')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

searchString = input("Add your search word here:")

string_no_rt = searchString + "-filter:retweets"
cursor = tweepy.Cursor(api.search, q=string_no_rt , count=20, lang="en", tweet_mode='extended')

maxCount = 5
count = 0
for tweet in cursor.items():    
    print()
    print("Tweet Information")
    print("================================")
    print("Text: ", tweet.full_text)
    print()

    print("User Information")
    print("================================")
    print("Location: ", tweet.user.location)
    print("Coordinates: ", tweet.coordinates)
    print("Geo Enabled? ", tweet.user.geo_enabled)

    count = count + 1
    if count == maxCount:
        break