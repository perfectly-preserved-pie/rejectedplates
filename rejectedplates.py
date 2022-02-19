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

for plate in maryland_2013.itertuples():
    client.create_tweet(text=plate[1])
    # Update the "Posted?" column for each row
    # https://www.skytowner.com/explore/updating_a_row_while_iterating_over_the_rows_of_a_dataframe_in_pandas
    maryland_2013.at[plate.Index, "Posted?"] = 'Yes'
    time.sleep(3600) # sleep for one hour

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