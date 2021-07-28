import os
import tweepy as tw
import pandas as pd
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
import gspread as gs
import gspread_dataframe as gd
import sys
import time
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


GSPREADSHEET = os.environ.get('GSPREADSHEET')
SEARCH_RESULT_SHEET = os.environ.get('SEARCH_RESULT_SHEET')
COUNTLOC_TWEETS_SHEET = os.environ.get('COUNTLOC_TWEETS_SHEET')


def main():
    """
    Get Twitter API keys, get input data, assign variable
    to geo_location function and call search_tweets and update_worksheet.
    """
    print("\nWelcome to Search your Brand on Twitter!\n")

    try:
        country = input("Write your country: \n ")
        if not country:
            print("\nCountry parameter cannot be empty\n")
            raise Exception

        city = input("\nWrite your city: \n"
                     "If your city has more than 1 word, please, use quotes.\n"
                     "Example: 'Rio de Janeiro' \n ")
        if not city:
            print("\nCity parameter cannot be empty\n")
            raise Exception

        keyword = input("\nWrite your search keyword: \n"
                        "If you would like to add more than one keyword, "
                        "please, use quotes. \n ")
        if not keyword:
            print("\nKeyword parameter cannot be empty.")
            raise Exception

        language = input("\nChoose your language: \n[en/es/pt/de] \n "
                         ).lower()
        if language not in ["en", "es", "pt", "de"]:
            print(
                "\nSelected language not supported. Default to en.\n")
            language = "en"
    except Exception:
        print("Fatal Error: Required parameter missing.\n")
        if input("Do you like to restart? [yes/no]: \n "
                 ).lower() == "yes":
            main()
        else:
            sys.exit(1)

    loc = geo_location(city, country)
    print(f'\nUser defined location: "{loc} \n ')
    time.sleep(2)

    print(f'This is your tweets search results based on your parameters:\n\n'
          f' Keyword: {keyword.capitalize()}\n'
          f' Country: {country.capitalize()}\n'
          f' City: {city.capitalize()}\n'
          f' Language: {language}')

    output = input("\nWould you like to print outputs?\n[yes/no] \n ")
    print('\nPreparing your data...\n')
    
    # Call search_tweet function to retrieve tweets
    tweets_df, search_result = search_tweet(
        loc, city, country, keyword, language, output)

    # Generate dataframe with tweet count by location
    count_loc = tweet_location_count(tweets_df, city, country, keyword, output)

    g_save = input('Would you like to save data on Google Spreadsheets?\n'
                   '[yes/no]?\n')

    # Connect on google spreadsheets
    try:
        creds = json.loads(os.environ.get('CREDS'))
        gc = gs.service_account_from_dict(creds, scopes=SCOPE)
    except Exception as e_Oauth:
        print(f'\nSorry, Oauth failed.\nError: {e_Oauth}\n'
              f'Please check your Google Credentials if you want to save your '
              f'data on google spreadsheets.\n')

    # Store data search your brand spreadsheet
    if g_save.lower() == "yes":
        try:
            update_worksheet(gc, SEARCH_RESULT_SHEET, search_result)
            update_worksheet(gc, COUNTLOC_TWEETS_SHEET, count_loc)
            print(f'\nYour Tweets location table is saved on Google Spreadsheets'
              f' file: {GSPREADSHEET}.')
            tweets_location_link = "https://bit.ly/3iTDCH1"
            print(f'{tweets_location_link}\n')
        except Exception:
            print("Unable to save into worksheet.")
       
    sys.exit(0)


def geo_location(city, country):
    """
    Get user location (by city and country) and  assign to geolocator
    and geocode
    """

    try:
        print(f"\nFinding geolocation for city: {city.capitalize()},"
              f" country: {country.capitalize()}")
        geolocator = Nominatim(user_agent="my_user_agent")
        geoloc = {'city': city, 'country': country}
        loc = geolocator.geocode(geoloc)

        if loc is None:
            raise Exception
        else:
            return loc
    except Exception:
        print("\nFatal Error: Unable to resolve country and city for"
              " geolocation.")
        if input("Do you like to restart? [yes/no]: \n").lower() == "yes":
            main()
        else:
            sys.exit(1)


def search_tweet(loc, city, country, keyword, language, output):
    """
    Gets user's latitude and longitude, filters retweets, and search tweets on
    Twitter in max range of 100km. Enable user to add search keyword,
    preferred language and outputs search date, keyword and language chosen,
    tweet create date, text, username and location. Rename columns to user
    friendly names and restrict dataframes to maximum 15 rows.
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
        # Json from twitter with all data
        json_data = [r._json for r in tweets.items()]
        # Dataframe created from twitter json
        df = pd.json_normalize(json_data)
        # Add columns to tweets dataframe with user data 
        df['Keyword'] = keyword
        df['Language'] = language
        df['Search Date'] = pd.to_datetime("today")
        # Select few columns from tweets dataframe 
        tweet_subset = (df[[
            'Keyword',
            'Language',
            'user.screen_name',
            'full_text',
            'user.location',
            'created_at',
            'Search Date']])
        tweets_df = tweet_subset.copy()
        # Rename columns to user friendly names
        tweets_df.rename(columns={
                    'created_at': 'Created at',
                    'user.screen_name': 'Username',
                    'full_text': 'Tweet',
                    'user.location': 'Location'},
                    inplace=True)
        if output.lower() == "yes":
            print(f' Tweets based on your search.\n\n {tweets_df[:15]}')

        return tweets_df, tweets_df[:15]

    except Exception as e_tweets:
        print(f'{"Sorry, an error has occured: "}\n{e_tweets} \n'
              f'{"Check your Twitter API keys."}\n')
        sys.exit(0)
    else:
        return tweets_df, (tweets_df[:15])


def tweet_location_count(tweets_df, city, country, keyword, output):
    """
    Gets tweets and group by location, create a count column with number of
    users on that location and sort values. Add Keyword and Seach Date column.
    """

    try:
        # Group tweets by location, count and sort values
        my_location = tweets_df.groupby("Location")
        my_location_grouped = my_location["Location"].count().sort_values(
            ascending=False).reset_index(name="Number of Users")
        # Add columns to dataframe with user input data
        my_location_grouped['Keyword'] = keyword
        my_location_grouped['Search Date'] = pd.to_datetime("today")
        my_location_rearranged = my_location_grouped[[
            'Keyword', 'Location', 'Number of Users', 'Search Date']]
        
        if output.lower() == "yes":
            print(f'\n{"Summary of Tweets by Location"}\n\n'
                  f' {my_location_rearranged[:15]}\n')

        return my_location_rearranged[:15]

    except Exception as e_location_count:
        print(f'{"An error has ocurred: "}{e_location_count}'
              f'\n{"We cannot deliver tweets by location table."}\n')


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
