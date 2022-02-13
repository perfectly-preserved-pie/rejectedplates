import pandas as pd
import tweepy
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Set up Tweepy
# You can provide the consumer key and secret with the access token and access
# token secret to authenticate as a user
client = tweepy.Client(
    consumer_key=os.getenv('consumer_key'), consumer_secret=os.getenv('consumer_secret'),
    access_token=os.getenv('access_token'), access_token_secret=os.getenv('access_token_secret')
)

# Import the CSV with some special flags to handle weird encoding
# https://stackoverflow.com/a/61267213
df = pd.read_csv("https://raw.githubusercontent.com/perfectly-preserved-pie/rejectedplates/main/States/2013-Maryland.csv") 

# Refer to the only column that matters
# https://stackoverflow.com/a/13758846
df = df[['Objectional Vanity Plates']]

# Sort the dataframe alphabetically from A to Z
df.sort_values(by='Objectional Vanity Plates', ascending=True, inplace=True)

# Update the bio
# https://docs.tweepy.org/en/stable/api.html#tweepy.API.update_profile
bio = "A Twitter bot that posts rejected personalized (vanity) license plate requests. Currently working through Maryland's 2013 list of rejected license plates. Made by @lookingstupid."
client.update_profile(description=bio)

for plate in df.itertuples():
    client.create_tweet(text=plate[1])