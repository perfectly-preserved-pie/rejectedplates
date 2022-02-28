import pandas as pd
import tweepy
import logging
import os

# Enter in Twitter ID
# https://developer.twitter.com/en/docs/twitter-ids
# Easy way of looking it up: https://tweeterid.com/
twitter_id = '1489107102610063363'

# Set up Tweepy
# You can provide the consumer key and secret with the access token and access token secret to authenticate as a user
# Heroku config vars: https://stackoverflow.com/a/32321268
client = tweepy.Client(
	consumer_key=os.environ.get('consumer_key'), consumer_secret=os.environ.get('consumer_secret'),
	access_token=os.environ.get('access_token'), access_token_secret=os.environ.get('access_token_secret')
)
# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(os.environ.get('consumer_key'), os.environ.get('consumer_secret'))
# set access to user's access key and access secret 
auth.set_access_token(os.environ.get('access_token'), os.environ.get('access_token_secret'))
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

# Update the bio
# https://docs.tweepy.org/en/stable/api.html#tweepy.API.update_profile
api.update_profile(description="A Twitter bot that posts rejected personalized (vanity) license plate requests. Currently working through Maryland's 2013 list of rejected license plates. Made by @lookingstupid.")

# Get the place ID so we can geotag the tweet
place_id = api.search_geo(granularity='admin',query='Maryland')[0].id

for plate in maryland_2013.itertuples():
	try:
		# Get the most recent 10 tweets
		tweets = client.get_users_tweets(id=twitter_id,user_auth=True)
	except tweepy.TweepError as e:
		logging.error(f"Couldn't get the last 10 tweets because {e.reason}")
		continue # Skip this iteration of the for loop and continue to the next one
	# Create an empty list 
	tweets_list = []
	# Iterate over the tweets and add the tweet text to the empty list we just created
	for tweet in tweets.data:
		tweets_list.append(tweet.text)
	# Iterate over the new list. If the license plate we're about to post doesn't already exist, post it to Twitter
	if plate[1] not in tweets_list:
		try:
			client.create_tweet(text=plate[1],place_id=place_id)
			logging.info(f"{plate[1]} has been tweeted.")
		except tweepy.TweepError as e: # if it fails, log it and continue on
			logging.error(f"Couldn't post {plate[1]} because {e.reason}")
	elif plate[1] in tweets_list:
		logging.warning(f"{plate[1]} was already tweeted, skipping...")