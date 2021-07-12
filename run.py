# python code goes here
import os
import tweepy as tw
from geopy.geocoders import Nominatim
from dotenv import load_dotenv


load_dotenv()
"""
Twitter API keys
"""
consumer_key = os.environ.get('API_KEY')
consumer_secret = os.environ.get('API_SECRET_KEY')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

"""
 Code inspired and partially on earthdatascience.org and
 ideoforms (https://www.erase.net/code/)
"""


def geo_location():
    """
    Get user location (by city and country) and outputs latitude and longitude
    """
    geolocator = Nominatim(user_agent="my_user_agent")
    city = input("Insert your city: \n")
    country = input("Insert your country: \n")
    loc = geolocator.geocode(city + ',' + country)
    return loc


def search_tweet():
    """
    Search tweets on Twitter in max range of 100km of user
    location, enable user to add search keyword, preferred
    language and outputs tweet text, tweet username, tweet
    location, tweet coordenation and if geolocaton is
    enable.
    """
    loc = geo_location()
    latitude = loc.latitude
    longitude = loc.longitude
    search_words = input("Add your keyword here: \n")
    language_search = input("Add your prefered language here: \n")
    new_search = search_words + "-filter:retweets"

    max_range = 100
    tweets = tw.Cursor(
                  api.search,
                  q=new_search,
                  count=1000,
                  lang=language_search,
                  geocode="%f,%f,%dkm" % (latitude, longitude, max_range),
                  tweet_mode='extended')

    maxCount = 5
    count = 0
    for tweet in tweets.items():
        if tweet.user.geo_enabled:
            print()
            print("Tweet Information")
            print("================================")
            print("Text: ", tweet.full_text)
            print()

            print("User Information")
            print("================================")
            print("Username:", tweet.user.name)
            print("Location: ", tweet.user.location)
            print("Coordinates: ", tweet.coordinates)
            print("Geo Enabled? ", tweet.user.geo_enabled)

        count = count + 1
        if count == maxCount:
            break


search_tweet()
