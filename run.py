import os
import tweepy as tw
import pandas as pd
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
import gspread as gs
import gspread_dataframe as gd
import sys
import time
from google.oauth2.service_account import Credentials
import json
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
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

creds = json.loads(os.environ.get('CREDS'))
GSPREADSHEET = os.environ.get('GSPREADSHEET')
SEARCH_RESULT_SHEET = os.environ.get('SEARCH_RESULT_SHEET')
COUNTLOC_TWEETS_SHEET = os.environ.get('COUNTLOC_TWEETS_SHEET')



def main():
    """
    Get Twitter API keys, get input data, assign variable
    to geo_location function and call search_tweets and update_worksheet.
    """
    print(f'\n{" Welcome to Search your Brand on Twitter!"}\n')

    country = input("\n Write your country: \n ").capitalize()
    city = input("\n Write your city: \n ").capitalize()
    keyword = input("\n Write keyword: \n ")
    language = input(
        "\n Choose your language: \n Please, use abreviation. Example: en \n "
        ).lower()

    if len(language) > 2:
        print('You wrote too many characters.\n'
              'Please, add your language abreviation')
        language = input('\n').lower()

    loc = geo_location(city, country)
    print(f'\n User defined location: "{loc} \n')
    time.sleep(2)

    print(f' This is your tweets search results based on your arguments:\n\n'
          f' Keyword: {keyword}\n'
          f' Country: {country}\n'
          f' City: {city}\n'
          f' Language: {language}')

    output = input("\n Would you like to print outputs? [yes/no]\n ")
    print('\n Preparing your data...')
    time.sleep(2)

    # call search_tweet function to retrieve tweets
    tweets_df, search_result = search_tweet(
        loc, city, country, keyword, language, output)
    # Generate dataframe with tweet count by location
    count_loc = tweet_location_count(tweets_df, city, country, keyword, output)

    g_save = input('\n Do you like to save data on Google Spreadsheets? [yes/no]?')
    print(g_save)
    try:
        #gc = gs.service_account(filename="creds.json")
        gc = gs.service_account_from_dict(creds,scopes=SCOPE)
        #GSPREAD_CLIENT = gs.authorize(SCOPED_CREDS)

    except Exception as e_Oauth:
        print(f'\nSorry, Oauth failed.\nError: {e_Oauth}\n'
              f'Please check your CREDS.json file if you want to save your '
              f'data on google spreadsheets.\n')

    # Store data search your brand spreadsheet
    if g_save == 'yes':
        try:
            update_worksheet(gc, SEARCH_RESULT_SHEET, search_result)
            update_worksheet(gc, COUNTLOC_TWEETS_SHEET, count_loc)
        except Exception:
            print("Unable to save into worksheet")


def geo_location(city, country):
    """
    Get user location (by city and country) and  assign to geolocator
    and geocode
    """

    try:
        print(f"\n Finding geolocation for city: {city}, country: {country}")
        geolocator = Nominatim(user_agent="my_user_agent")
        geoloc = {'city': city, 'country': country}
        loc = geolocator.geocode(geoloc)

        if loc is None:
            raise Exception
        else:
            return loc
    except Exception:
        print('\n Fatal Error: Unable to resolve country and city for'
              ' geolocation.')
        if input('Do you like to restart? [yes/no]: ') == "yes":
            main()
        else:
            sys.exit(1)

    sys.exit(0)


def search_tweet(loc, city, country, keyword, language, output):
    """
    Gets user's latitude and longitude, filters retweets, and search tweets on
    Twitter in max range of 100km. Enable user to add search keyword,
    preferred language and outputs search date, keyword and language chosen,
    tweet create date, text, username and location. Rename columns to user
    friendly names and restrict dataframe to maximum 15 rows.
    """

    new_search = keyword + "-filter:retweets"

    max_range = 100

    try:
        tweets = tw.Cursor(
                      api.search,
                      q=new_search,
                      count=1000,
                      lang=language,
                      geocode="%f,%f,%dkm" %
                      (float(loc.latitude), float(loc.longitude), max_range),
                      tweet_mode='extended')

        json_data = [r._json for r in tweets.items()]
        df = pd.json_normalize(json_data)
        df['Keyword'] = keyword
        df['Language'] = language
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
                    'full_text': 'Tweet',
                    'user.location': 'Location'},
                    inplace=True)
        if output == "yes":
            print(f'\n\n Tweets based on your search.\n'f'\n {tweets_df[:15]}')

        return tweets_df, tweets_df[:15]

    except Exception as e_tweets:
        print("Sorry, an error has occured: \n", e_tweets)
        sys.exit(0)
    else:
        return tweets_df, (tweets_df[:15])


def tweet_location_count(tweets_df, city, country, keyword, output):
    """
    Gets tweets and group by location, create a count column with number of
    users on that location and sort values. Add Keyword and Seach Date column.
    """

    try:
        my_location = tweets_df.groupby("Location")
        my_location_grouped = my_location["Location"].count().sort_values(
            ascending=False).reset_index(name="Number of Users")
        my_location_grouped['Keyword'] = keyword
        my_location_grouped['Search Date'] = pd.to_datetime("today")
        my_location_rearranged = my_location_grouped[[
            'Search Date', 'Keyword', 'Location', 'Number of Users']]
        time.sleep(3)

        if output == "yes":
            print(f'  \n\nSummary of Tweets by Location\n\n'
                  f' {my_location_rearranged}')

        return my_location_rearranged

    except Exception as e_location_count:
        print(f'An error has ocurred: {e_location_count}'
              f'\nWe cannot deliver tweets by location table.')


def update_worksheet(gc, p_sheet, p_search_result):
    """
    Update spreadsheet.
    """

    ws = gc.open(GSPREADSHEET).worksheet(p_sheet)
    existing = gd.get_as_dataframe(ws)
    updated = existing.append(p_search_result)
    gd.set_with_dataframe(ws, updated)


if __name__ == "__main__":
    main()
