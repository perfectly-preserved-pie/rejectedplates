import pandas as pd
import tweepy
import time
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Set up logging to a file
# https://docs.python.org/3/howto/logging.html#logging-to-a-file
logging.basicConfig(filename='rejectedplates.log', encoding='utf-8', level=logging.DEBUG)

# Set up Tweepy
# You can provide the consumer key and secret with the access token and access
# token secret to authenticate as a user
client = tweepy.Client(
    consumer_key=os.getenv('consumer_key'), consumer_secret=os.getenv('consumer_secret'),
    access_token=os.getenv('access_token'), access_token_secret=os.getenv('access_token_secret')
)
# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(os.getenv('consumer_key'), os.getenv('consumer_secret'))
# set access to user's access key and access secret 
auth.set_access_token(os.getenv('access_token'), os.getenv('access_token_secret'))
# calling the api 
api = tweepy.API(auth)

## Maryland 2013
# Import the CSV from GitHub
maryland_2013 = pd.read_csv("https://raw.githubusercontent.com/perfectly-preserved-pie/rejectedplates/main/States/2013-Maryland.csv") 

# Refer to the only column that matters
# https://stackoverflow.com/a/13758846
maryland_2013 = maryland_2013[['Objectional Vanity Plates']]

# Sort the dataframe alphabetically from A to Z
maryland_2013.sort_values(by='Objectional Vanity Plates', ascending=True, inplace=True)

# Add an empty column so we can keep track of what's been posted
maryland_2013["Posted?"] = ''

# Update the bio
# https://docs.tweepy.org/en/stable/api.html#tweepy.API.update_profile
api.update_profile(description="A Twitter bot that posts rejected personalized (vanity) license plate requests. Currently working through Maryland's 2013 list of rejected license plates. Made by @lookingstupid.")

# Get the most recent 10 tweets
tweets = client.get_users_tweets(id='1489107102610063363',max_results=100,user_auth=True)
# Create an empty list 
tweets_list = []
# Iterate over the tweets and add the tweet text to the empty list we just created
for tweet in tweets.data:
	tweets_list.append(tweet.text)
	
for plate in maryland_2013.itertuples():
    # Iterate over the new list. If the license plate we're about to post doesn't already exist, post it to Twitter
    if plate[1] not in tweets_list:
        try:
            client.create_tweet(text=plate[1])
            time.sleep(3600) # sleep for one hour
        except tweepy.TweepError as e: # if it fails, log it and continue on
            logging.error(f"Couldn't post {plate[1]} because {e.reason}")
    elif plate[1] in tweets_list:
        logging.warning(f"{plate[1]} was already tweeted, skipping...")

## Massachusetts 2013
massachusetts_2013 = pd.read_csv("https://raw.githubusercontent.com/perfectly-preserved-pie/rejectedplates/main/States/2013-Massachusetts.csv") 
massachusetts_2013 = massachusetts_2013[['Plate Number']]
massachusetts_2013.sort_values(by='Plate Number', ascending=True, inplace=True)
massachusetts_2013["Posted?"] = ''
api.update_profile(description="A Twitter bot that posts rejected personalized (vanity) license plate requests. Currently working through Massachusetts's 2013 list of rejected license plates. Made by @lookingstupid.")
for plate in massachusetts_2013.itertuples():
    client.create_tweet(text=plate[1])
    massachusetts_2013.at[plate.Index, "Posted?"] = 'Yes'
    time.sleep(3600) # sleep for one hour

## New Jersey 2013
newjersey_2013 = pd.read_csv("https://raw.githubusercontent.com/perfectly-preserved-pie/rejectedplates/main/States/2013-NewJersey.csv") 
newjersey_2013 = newjersey_2013[['OBJ_STRING']]
newjersey_2013.sort_values(by='OBJ_STRING', ascending=True, inplace=True)
newjersey_2013["Posted?"] = ''
api.update_profile(description="A Twitter bot that posts rejected personalized (vanity) license plate requests. Currently working through New Jersey's 2013 list of rejected license plates. Made by @lookingstupid.")
for plate in newjersey_2013.itertuples():
    client.create_tweet(text=plate[1])
    newjersey_2013.at[plate.Index, "Posted?"] = 'Yes'
    time.sleep(3600) # sleep for one hour

## New York 2013
newyork_2013 = pd.read_csv("https://raw.githubusercontent.com/perfectly-preserved-pie/rejectedplates/main/States/2013-NewYork.csv") 
newyork_2013 = newyork_2013[['Requested Plate Configuration']]
newyork_2013.sort_values(by='Requested Plate Configuration', ascending=True, inplace=True)
newyork_2013["Posted?"] = ''
api.update_profile(description="A Twitter bot that posts rejected personalized (vanity) license plate requests. Currently working through New Jersey's 2013 list of rejected license plates. Made by @lookingstupid.")
for plate in newyork_2013.itertuples():
    client.create_tweet(text=plate[1])
    newyork_2013.at[plate.Index, "Posted?"] = 'Yes'
    time.sleep(3600) # sleep for one hour