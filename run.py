import os
import tweepy as tw
import pandas as pd
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
import argparse
import gspread as gs
import gspread_dataframe as gd
import sys
import time
load_dotenv()


def get_env_variable(var_name):
    """
    Get twitter API keys on .env file
    """
    try:
        return os.environ[var_name]
    except KeyError:
        print(f' \n {"Fatal Error:"} {var_name}'
              f' {"environment variable required"}\n')
        sys.exit(0)


"""
Twitter API keys
"""
API_KEY = get_env_variable('API_KEY')
API_SECRET_KEY = get_env_variable('API_SECRET_KEY')
ACCESS_TOKEN = get_env_variable('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = get_env_variable('ACCESS_TOKEN_SECRET')


"""
Setting up autenthication
"""
auth = tw.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)

"""
GoogleSpreadsheets API keys
"""
GSPREADSHEET = os.environ.get('GSPREADSHEET')
SEARCH_RESULT_SHEET = os.environ.get('SEARCH_RESULT_SHEET')
COUNTLOC_TWEETS_SHEET = os.environ.get('COUNTLOC_TWEETS_SHEET')

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


def get_args():

    """
    Get arguments and assign inputs if arguments are empty and
    run all the functions
    """
    # add description of task
    parser = argparse.ArgumentParser(
        description='Search for tweets by location and keyword')
    # add country argument
    parser.add_argument(
        '-co', '--country', type=str, help='Your country', required=True)
    # add city argument
    parser.add_argument(
        '-cy', '--city', type=str, help='Your city', required=True)
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
        help='Number of tweets added to your table', default=15)
    # save on google spreedsheets option
    parser.add_argument(
        '-gs', '--gsave', type=str, choices=['yes', 'no'],
        help='Save your data on Google Spreadsheet', default='yes')
    parser.add_argument(
        '-v', '--verbose', action="store_true", help='Print outputs')

    try:
        args = parser.parse_args()
    except SystemExit:
        print("\n\nPlease see help below:")
        parser.print_help()
        sys.exit(0)
    except Exception as e:
        print('Sorry an unknown error occurred. Exception: %s', e)
    return args


def main():
    """
    Get Twitter API keys, call argparse from get_args, assign variable
    to geo_location function and call search_tweets and update_worksheet.
    """
    parsed_args = get_args()
    loc = geo_location(parsed_args)
    print(f'\n Welcome to Search your Brand on Twitter!\n\n'
          f'{" User defined location: "}{loc} \n')
    time.sleep(2)

    print(f' This is your tweets search results based on your arguments:\n\n'
          f' Keyword: {parsed_args.keyword}\n'
          f' Country: {parsed_args.country}\n'
          f' City: {parsed_args.city}\n'
          f' Language: {parsed_args.language}')
 
    time.sleep(2)

    tweets_df, search_result = search_tweet(loc, parsed_args)
 
    print(f'\nYour Tweets table is saved on Google Spreadsheets file: {GSPREADSHEET}.'
          f' and worksheet: {SEARCH_RESULT_SHEET}')
  
    count_loc = tweet_location_count(tweets_df, parsed_args)

    print(f'\nYour Tweets location table is saved on Google Spreadsheets file: {GSPREADSHEET}'
          f' and worksheet: {COUNTLOC_TWEETS_SHEET}.')

    try:
        gc = gs.service_account(filename="creds.json")
    except Exception as e_Oauth:
        print(f'\nSorry, Oauth failed.\nError: {e_Oauth}\n'
              f'Please check your creds.json file if you want to save your '
              f'data on google spreadsheets.\n')
        parsed_args.gsave = 'no'

    if parsed_args.gsave == 'yes':
        update_worksheet(gc, SEARCH_RESULT_SHEET, search_result)
        update_worksheet(gc, COUNTLOC_TWEETS_SHEET, count_loc)


def geo_location(args):
    """
    Get user location (by city and country) and  assign the args to variables
    with geolocator and geocode
    """

    try:
        geolocator = Nominatim(user_agent="my_user_agent")
        geoloc = {'city': args.city, 'country': args.country}
        loc = geolocator.geocode(geoloc)

        if loc is None:
            raise Exception
        else:
            return loc
    except Exception as e_geoloc:
        e_geoloc.message = '\n Fatal Error: Unable to resolve country and'
        'city for geolocation. \n Please review your parameters \n'
        print(e_geoloc.message)
        sys.exit(0)


def search_tweet(loc, args):
    """
    Gets user's latitude and longitude and search tweets on Twitter in max
    range of 100km, enable user to add search keyword, preferred language 
    and outputs tweet text, tweet username, and outputs tweet location, tweet
    coordenation and if geolocaton is enable.
    """

    new_search = args.keyword + "-filter:retweets"

    max_range = 100

    try:
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
        df['Keyword'] = args.keyword
        df['Language'] = args.language
        df['Search Date'] = pd.to_datetime("today")
        tweet_subset = (df[[
            'Search Date',
            'Keyword',
            'Language',
            'created_at',
            'user.screen_name',
            'full_text',
            'user.location']])
        tweets_df = tweet_subset.copy()
        tweets_df.rename(columns={
                    'created_at': 'Created at',
                    'user.screen_name': 'Username',
                    'full_text': 'Tweet', 'user.location': 'Location'},
                    inplace=True)
        if args.verbose:
            print(f'\n {tweets_df[:args.tweets]}')
        return tweets_df, tweets_df[:args.tweets]

    except Exception as e_tweets:
        print("Sorry, an error has occured: \n", e_tweets)
        sys.exit(0)
    else:
        return tweets_df, (tweets_df[:args.tweets])


def tweet_location_count(tweets_df, args):
    """
    Gets tweets and group by location, create a count column with number of
    users on that location and sort values. Add Keyword and Seach Date column.
    """

    try:
        my_location = tweets_df.groupby("Location")
        my_location_grouped = my_location["Location"].count().sort_values(
            ascending=False).reset_index(name="Number of Users")
        my_location_grouped['Keyword'] = args.keyword
        my_location_grouped['Search Date'] = pd.to_datetime("today")
        my_location_rearranged = my_location_grouped[[
            'Search Date', 'Keyword', 'Location', 'Number of Users']]
        time.sleep(3)

        if args.verbose:
            print(f'  \n\nSumary of Tweets by Location\n\n'
                f' {my_location_rearranged}')
        return my_location_rearranged

    except Exception as e_location_count:
        print(f'An error has ocurred: {e_location_count}'
              f'\nWe cannot deliver tweets by location table.')


def update_worksheet(gc, p_sheet, p_search_result):
    """
    Update spreadsheet, add new rows with the data created.
    """

    ws = gc.open(GSPREADSHEET).worksheet(p_sheet)
    existing = gd.get_as_dataframe(ws)
    updated = existing.append(p_search_result)
    gd.set_with_dataframe(ws, updated)


if __name__ == "__main__":
    main()
