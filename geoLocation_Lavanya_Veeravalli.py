"""
This prorgam generates word cloud and input for this script is the geo_location_frequency.csv generated from
live twitter analytics scipt twitterAnalysis_lavanya.py
"""
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

#Read geolocation frequency data
geo_frequency_df = pd.read_csv(r'C:\Users\results\geo_location_frequency.csv')

#convert the 'country' and '#counts' into dictionary as WordCloud requires a dict
geo_frequency_dict = dict(zip(geo_frequency_df['country'].tolist(), geo_frequency_df['#counts'].tolist()))

#generate word cloud
wc = WordCloud(background_color='white', width=800, height=400, max_words=200, collocations=False).generate_from_frequencies(geo_frequency_dict)

#Generate plot
plt.figure(figsize=(15, 15))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()