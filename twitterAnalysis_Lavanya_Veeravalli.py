"""
This program retrieves live tweets with KeyWord as "python" from Twitter and generates hash tag frequency 
and geolocation frequency and generates top 20 hashtags
This program will continue to run till the program gets interupted by the user or any connection error
"""

import tweepy
import json
import re
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import pandas as pd
from collections import Counter
from functools import reduce
import os


# authorization tokens
consumer_key = ' '
consumer_secret = ' '
access_key = ' '
access_secret = ' '

geo_location_list = []
hashtag_frequency_dict = {}
#Variable to plot top %no frequency of hashtags
view_top_hashtag_count = 20

# override tweepy.StreamListener to add logic to on_data
class MyStreamListener(tweepy.StreamListener):
      
    def on_data(self, data):
        all_hashtags = []
        # Load json data
        all_data = json.loads(data)
        # Key words to be filetred from tweet's text
        filterKeywords = ["python"]
        # Extract tweet text and convert into lowercase characters
        try:
            if all_data["text"] is not None:
                tweet_text = all_data["text"]
                tweet_text = tweet_text.lower()
        except KeyError:
            print("text not found in the tweet")
               
        # Count the #hashtags if "filterKeywords" is found in the tweet. While counting, eliminate non-alpha words,
        # single character words amd # filterKeywords
        if any([i for i in filterKeywords if i in tweet_text]):
            for word in tweet_text.split():
                if word.startswith('#'):
                    word = re.sub('[\W_]+', '', word)
                    if word not in filterKeywords and len(word) > 1:
                        all_hashtags.append(word)
            # Extract geo Location information from the tweet for geolocation ananlysis if abvailable for tweet
            # If the user has used format as "City, Country", then only "Country" will be added to geo_location
            # list for further ananlysis
            try: 
                if all_data["user"]["location"] is not None:
                    geo_location = all_data["user"]["location"]
                    geo_location = geo_location.replace(" ", "").lower()
                    if "," in geo_location:
                        geo_location = geo_location.split(",")[1]
                    geo_location = re.sub('[\W_]+', '', geo_location)
                    if geo_location.encode().isalpha():
                        geo_location_list.append(geo_location)
            except KeyError:
                print("location not found in the tweet")

        # Collect frequency counts for all the #hashtags
        for i in all_hashtags:
            if i not in hashtag_frequency_dict:
                hashtag_frequency_dict[i] = 1
            else:
                hashtag_frequency_dict[i] += 1
                
        # Write hashtag frequency into a csv file
        total_hashtag_frequency_file = r'C:\Users\results\total_hashtag_frequency.csv'
        csv_columns = ['hashtag','#counts']        
        with open(total_hashtag_frequency_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['hashtag','#counts'])
            for k, v in hashtag_frequency_dict.items():
                writer.writerow([k, v])
                
        # Count the number of countries from geo_location_list
        # Write geolocation as csv for further ananlysis
        geo_location_count_file =  r'C:\Users\results\geo_location_frequency.csv'
        sr = pd.Series(geo_location_list).value_counts().sort_values(ascending=False).reset_index()
        sr.columns = ['country', '#counts']
        sr.to_csv(geo_location_count_file, header=True, index=False, encoding='utf-8-sig')

        # Plot the frequency count for top counted hashtags
        if hashtag_frequency_dict:
            top_15_hashtags = []
            top_15_hashtags = {key: value for key, value in sorted(hashtag_frequency_dict.items(), key=lambda item: item[1], reverse=True)[:view_top_hashtag_count:]}          
            style.use('fivethirtyeight')
            fig = plt.figure(figsize=(15,3))          
            ax1 = fig.add_subplot(1,1,1)
            ax1.tick_params(labelsize=12)
            def animate(d):
                keys = list(top_15_hashtags.keys())
                values = list(top_15_hashtags.values())
                ax1.clear()
                plt.xticks(rotation=45)
                ax1.bar(keys, values)
            ani = animation.FuncAnimation(fig, animate, interval=2000)
            fig1=plt.gcf()
            plt.show()
            hashtag_frequency_image_file = r"C:\Users\results\top_hashtag_frequency.jpg"
            fig1.savefig(hashtag_frequency_image_file, bbox_inches="tight")     
        return True    
    def on_error(self, status_code):
        if status_code == 420:
            return Flase
        print("Encountered streaming error (", status_code, ")")
        return True
    def on_timeout(self):
        print("Timeout issue")
        return True
    def on_exception(self, exception):
        print(exception)
        return True
               
if __name__ == "__main__":
    # complete authorization and initialize API endpoint
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize stream and add filter for Keywords and language as English
    myStreamListener = MyStreamListener()
    mystream = tweepy.Stream(auth=api.auth, listener=myStreamListener,tweet_mode='extended')
    #KeyWord to filter
    tags = ["python"]            
    mystream.filter(track=tags, languages=["en"])