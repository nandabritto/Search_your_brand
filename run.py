# python code goes here
import os
import tweepy as tw
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
import argparse


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


def main():
    parser = argparse.ArgumentParser(
        description='search for tweets by location and \
                     keyword')
    parser.add_argument(
        '--city', type=str, help='Your city')
    parser.add_argument(
        '--country', type=str, help='Your country')
    args = parser.parse_args()
    print(args)
    if not args.city:
        args.city = input("Insert your city \n")
    if not args.country:
        args.country = input("Insert your country \n")
    loc = geo_location(args)
    print(loc)
    search_tweet(loc)


"""
 Code inspired and partially on earthdatascience.org and
 ideoforms (https://www.erase.net/code/)
"""


def geo_location(args):
    """
    Get user location (by city and country) 
    """

    geolocator = Nominatim(user_agent="my_user_agent")
    loc = geolocator.geocode(args.city + ',' + args.country)
    return loc


def search_tweet(loc):
    """
    Gets user's latitude and longitude and search tweets
    on Twitter in max range of 100km, enable user to add
    search keyword, preferred language and outputs tweet
    text, tweet username, and outputs tweet location,
    tweet coordenation and if geolocaton is enable.
    """

    search_words = input("Add your keyword here: \n")
    language_search = input("Add your prefered language here: \n")
    new_search = search_words + "-filter:retweets"

    max_range = 100
    tweets = tw.Cursor(
                  api.search,
                  q=new_search,
                  count=1000,
                  lang=language_search,
                  geocode="%f,%f,%dkm" %
                  (float(loc.latitude), float(loc.longitude), max_range),
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


main()
