import pandas as pd
import tweepy
import time

# Set up Tweepy
consumer_key = input("Please enter the consumer key:\n")
consumer_secret = input("Please enter the consumer secret:\n")
access_token = input("Please enter the access_token:\n")
access_token_secret = input("Please enter the access_token_secret:\n")

# You can provide the consumer key and secret with the access token and access
# token secret to authenticate as a user
client = tweepy.Client(
    consumer_key=f"{consumer_key}", consumer_secret=f"{consumer_secret}",
    access_token=f"{access_token}", access_token_secret=f"{access_token_secret}"
)

# Import the CSV with some special flags to handle weird encoding
# https://stackoverflow.com/a/61267213
df = pd.read_csv("/mnt/c/Users/lunar/Downloads/vanity/2013-Maryland.csv") 

# Refer to the only column that matters
# https://stackoverflow.com/a/13758846
df = df[['Objectional Vanity Plates']]

# Sort the dataframe alphabetically from A to Z
df.sort_values(by='Objectional Vanity Plates', ascending=True, inplace=True)

# Update the bio
# https://docs.tweepy.org/en/stable/api.html#tweepy.API.update_profile
bio = "A Twitter bot that posts rejected personalized license plate requests. Made by @lookingstupid. Currently working through Maryland's 2013 list of rejected license plates."
client.update_profile(description=bio)

for plate in df.itertuples():
    client.create_tweet(text=plate[1])
    time.sleep(3600) # sleep for one hour