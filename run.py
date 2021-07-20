# python code goes here
import os
import tweepy as tw
import pandas as pd
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
import argparse
import gspread as gs
import gspread_dataframe as gd
import sys
import collections
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

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


"""
GoogleSpreadsheets API keys
"""

gc = gs.service_account(filename="creds.json")


def get_args():

    """
    Get arguments and assign inputs if arguments are empty and
    run all the functions
    """
    # add description of task
    parser = argparse.ArgumentParser(
        description='Search for tweets by location and keyword')
    # add city argument
    parser.add_argument(
        '-cy', '--city', type=str, help='Your city', required=True)
    # add country argument
    parser.add_argument(
        '-co', '--country', type=str, help='Your country', required=True)
    # add keyword argument
    parser.add_argument(
        '-key', '--keyword', type=str, help='Your keyword', required=True)
    # add language argument
    parser.add_argument(
        '-ln', '--language', type=str, help='Your preferred language',
        default='en')
    # add number of tweets argument
    parser.add_argument(
        '-tw', '--tweets', type=int,
        help='Number of tweets added to your table', default=10)
    # to be interactivity mode

    try:
        args = parser.parse_args()
    except SystemExit:
        print("\n\nPlease see help below:")
        parser.print_help()
        sys.exit(0)
    return args


def main():
    """
    Call argparse from get_args, assign variable to geo_location function and
    call search_tweets and update_worksheet
    """

    parsed_args = get_args()
    loc = geo_location(parsed_args)
    print(loc)
    tweets_df,search_result = search_tweet(loc, parsed_args)
    update_worksheet(search_result)
    tweet_location_count(tweets_df,parsed_args)
    


def geo_location(args):
    """
    Get user location (by city and country) and  assign the args to variables
    with geolocator and geocode
    """

    geolocator = Nominatim(user_agent="my_user_agent")
    loc = geolocator.geocode(args.city + ',' + args.country)
    return loc


def search_tweet(loc, args):
    """
    Gets user's latitude and longitude and search tweets
    on Twitter in max range of 100km, enable user to add
    search keyword, preferred language and outputs tweet
    text, tweet username, and outputs tweet location,
    tweet coordenation and if geolocaton is enable.
    """

    new_search = args.keyword + "-filter:retweets"

    max_range = 100
    tweets = tw.Cursor(
                  api.search,
                  q=new_search,
                  count=1000,
                  lang=args.language,
                  geocode="%f,%f,%dkm" %
                  (float(loc.latitude), float(loc.longitude), max_range),
                  tweet_mode='extended')
    json_data = [r._json for r in tweets.items() if r.user.geo_enabled]
    df = pd.json_normalize(json_data)
    tweet_subset = (df[[
        'created_at',
        'user.screen_name',
        'full_text',
        'user.location']])
    tweets_df = tweet_subset.copy()
    tweets_df.rename(columns={
        'created_at': 'Created at',
        'user.screen_name': 'Username',
        'full_text': 'Tweet',
        'user.location': 'Location'},
         inplace=True)
    print(tweets_df[:args.tweets])
    return tweets_df, (tweets_df[:args.tweets])

def tweet_location_count(tweets_df,args):
    my_location = tweets_df.groupby("Location")
    print(my_location["Location"].count().sort_values(ascending=False))

def update_worksheet(p_search_result):
    """
    Update sales worksheet, add new row with the dataframe created
    """

    ws = gc.open("search_your_brand").worksheet("tweets")
    existing = gd.get_as_dataframe(ws)
    updated = existing.append(p_search_result)
    gd.set_with_dataframe(ws, updated)


main()
