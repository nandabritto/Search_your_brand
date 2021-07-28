<h1 align=center> Search your brand on Twitter</h1>

<p align=center>If you would like to check how your brand is being commented on Twitter, this is your app! 

Search youur brand will search tweets containeing your preferred keyword in a 100km max range from you defined location and return to you a table with user's information, tweet content and where is the location with more results of your keyword. <br>
 </p>

<img src="images/readme_images/search_your_brand_mock_up.png">

Live app link [here](https://search-your-brand.herokuapp.com/)

 ## Project Purpose

Create an app that can search tweets using Twitter API and outputs tweets with chosen keyword in a max range of 100km. Also create a table data with all tweets location grouped and counted.   Data created can be viewed on Terminal or storage on Google Spreadsheets. 

## User Experience

### User Stories

+ As a user, I would like to be able to …

1. easily add my preferred information as City, Country, language and keyword;
2. easily check if my information are correct;
3. decide if I want to get outputs on my command line or just save data on Google spreadsheets;
4. check my created data on Google Spreadsheet.

### App Owner Stories

+ As App Owner Stories, I would like to be able to provide …

1. a simple, straightforward intuitive user experience;
2. clear output data on command line or  cloud storage;
3. user's feedback in case of wrong input.

## Functional Scope 

The following flowchart shows the flow of "Search your brand" graphically.

<img src="images/readme_images/search your brand_flowchart.png">

## Features

#### Welcome message 

 Welcome user to app. 

<img src="images/readme_images/greetings.png">

#### User options
Ennable user to choose some options as Country, City, Keyword and Preferred Language. 

<img src="images/readme_images/options.png">

If City or Country options could't be validated by geolocation function the user has option to restart and try again. 

<img src="images/readme_images/testing/e_geoloc.png">

User can choose between four different languages to search on Twitter (English-en, Spanish-es, Portuguese-pt and German-de)
English language is set by default if user doen't want to set his own choice or write any wrong option. 

#### Returning user defined options.

<img src="images/readme_images/returning-inputs.png">

Allows user to review options setted to the app in order to search tweets and choose to get data output on command line or not.  
If user set yes all the data collected from Twitter will be print on command line. 

<img src="images/readme_images/output_tweets.png">
<img src="images/readme_images/output_tweetsloc.png">

Tweets table has some columns added from Twitter API (marked with a red line on image below) as: tweet creation date, tweet text, username and location. 
Search date, keyword and language were added to table (marked with a green line on image below)in order to add information about internal app search details. 

<img src="images/readme_images/tweets_table_explained.png">


## Future Features

I would like to ...

* ... return to use argparse modules to make it easy to write user-friendly command-line interfaces;
* ... add options to search data in different social medias as Instagram, Facebook and Tik Tok. 
* ... add user option to save data on different files formats as CSV and APACHE PARQUET.

## Languages Used

    Python 3.0

## Frameworks, Libraries & Programs Used

    Grammarly: Used to correct any mistakes on readme and app text.
    Git: Git was used for version control by utilizing the Gitpod terminal to commit to Git and Push to GitHub.
    GitHub: GitHub is used to store the projects code after being pushed from Git.
    Google Spreadsheets API: Used to storage Search table data. 
    Geopy: Used to locate user the coordinates based on city and country.
    Pandas: Used for data analyse and dataframe creation. 
    Tweepy: Used to access the Twitter API with Python. 
    Twitter API: Used to interact and get Tweets Data related with user keyword.

## Testing and Code validation 

All testing and code validation details are described in a separeted file called TESTING.mg and can be found [here](TESTING.md).

# Deployment 

This app is deployed using Heroku.

<details>
 <summary>### Heroku Deployment steps</summary>
 
 1. Ensure all dependencies are listed on requirements.txt. 
 
 Write on python terminal ` pip3 freeze > requirements.txt"` and a list with all requirements will be created to be read by Heroku. 
 
 2. Setting up your Heroku

    2.1 Go to heroku website (https://www.heroku.com/). 
	2.2 Login to Heroku and go to Create App.
<img src="images/readme_images/deployment/heroku_login.png">
<img src="images/readme_images/deployment/heroku_login2.png">
	2.3 Click in New and Create new app
<img src="images/readme_images/deployment/heroku_newapp.png">
	2.4 Choose a name and set your location
<img src="images/readme_images/deployment/heroku_createnewapp.png">
 	2.5. Navigate to the deploy tab
<img src="images/readme_images/deployment/heroku_dashboard_deploy.png">
  	2.6. Click in Connect to Github and Search for 'nandabritto' GitHub account and 'search_your_brand' repository
<img src="images/readme_images/deployment/heroku_github_deploy.png">
  	2.7.  Navigate to the settings tab
<img src="images/readme_images/deployment/heroku_dashboard_settings.png">
  	2.8.  Click on Config Vars, and add your Twitter and Google Sheets API keys, Google Spreadsheets file and worksheets names. 
<img src="images/readme_images/deployment/heroku_vars_settings.png">
 	2.9. Click on Add a buildpack on the same page. Select Python and node.js, ensuring Python is listed first after you save the changes.
<img src="images/readme_images/deployment/heroku_buildpacks_settings.png">
 
 3. Deployment on Heroku
   
 	3.1.  Navigate to the Deploy tab.
<img src="images/readme_images/deployment/heroku_dashboard_deploy.png">
	3.2.  Choose main branch to deploy and enable automatic deployment to build heroku everytime any changes ar push on repository.
<img src="images/readme_images/deployment/heroku_automatic_deploys.png">
    3.3 Click on manual deploy to build the app.  When complete, click on View to redirect to live site. 
<img src="images/readme_images/deployment/heroku_view.png">
</details>

<details>
<sumary>### Forking the GitHub Repository</sumary>

* By forking the GitHub Repository you will be able to make a copy of the original repository on your own GitHub account allowing you to view and/or make changes without affecting the original repository by using the following steps:

    Log in to GitHub and locate the GitHub Repository
    At the top of the Repository (not top of page) just above the "Settings" Button on the menu, locate the "Fork" Button.
    You should now have a copy of the original repository in your GitHub account.

* Making a Local Clone

    Log in to GitHub and locate the GitHub Repository
    Under the repository name, click "Clone or download".
    To clone the repository using HTTPS, under "Clone with HTTPS", copy the link.
    Open Git Bash
    Change the current working directory to the location where you want the cloned directory to be made.
    Type git clone, and then paste the URL you copied in Step 3.

$ git clone https://github.com/nandabritto/search_your_brand

    Press Enter. Your local clone will be created.
<details>

## Activating Google API Credential

API will allow our Python project to access and update data in our spreadsheet. 

<details>
<summary>API activating steps</summary>

    2.1 Go to google cloud website (https://cloud.google.com). 
	2.2 Sign in or login to google cloud and  click on the“Select a project and then select new project.
<img src="images/readme_images/deployment/google_api/start.png">
	2.3 Add your project name and click in create. 
<img src="images/readme_images/deployment/google_api/newproject.png">
	2.4 Navigate to API and Services
<img src="images/readme_images/deployment/google_api/google_list.png">
 	2.5. Click on Library
<img src="images/readme_images/deployment/google_api/llibrary.png">
  	2.6. First enable Google Drive API
	2.7 Second enable Google Sheets API.
	2.8 Click  in create credentials and fill out form. (Service account Id must be copied from your table on googlespread sheets share option)
<img src="images/readme_images/deployment/google_api/data_app.png">
	2.9 Click Application data button.
<img src="images/readme_images/deployment/google_api/app_details.png">
	2.10 Select I am not using them for compute engine,App engine or cloud platform.
	2.11 Then click next and then done button.
	2.12 Then go to ApIs and Services, click credential then can see a service account.
	2.13 Click the service account and Keys tab.
<img src="images/readme_images/deployment/google_api/keys.png"> 
	2.14 Click on the Add Key and select Create New Key. 
	2.15 Select JSON and then click Create. 
<img src="images/readme_images/deployment/google_api/jsonkey.png">
	2.16 This will trigger the json file with your API credentials in it to download to the computer. 
    2.17 Add on your gitpod space. Copy all information from this file and add to an .env file.
    ` CREDS = {all data from json file}`
</details>
