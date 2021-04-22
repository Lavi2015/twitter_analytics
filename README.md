# Real time twitter analytics

## Required packages
- tweepy
- matplotlib
- pandas

## Prerequisite
- Create twitter developer account
- Cerate an app and save Consumer Key, Consumer Secret, OAuth Access Token and OAuth Access Token Secret

## Program instructions
- *twitterAnalytics_Lavanya_Veeravalli.py* program retrieves live tweets with KeyWord as **python** from Twitter and generates hash tag frequency 
and geolocation frequency. It also generates top 20 hashtags.
- This program will continue to run till the program gets interupted by the user or any connection error.
- *view_top_hashtag_count* variable from twitterAnalytics_Lavanya_Veeravalli.py can be changed as per the requirements.
- *geoLocation_Lavanya_Veeravalli.py* generates word cloud and input for this script is the *geo_location_frequency.csv* generated from
live twitter analytics scipt *twitterAnalysis_lavanya.py*.
- User defined paths should be changed according to Windows or other environments. Example paths in the script should work on Windows.
