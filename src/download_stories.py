import argparse
import json
import urllib
from reddit.reddit_classes import *
from datetime import *
from reddit.reddit_client import RedditUrlOpener
import time
import os
import logging

REDDIT_URL='http://reddit.com'
OUTPUT_DIR='../data/'
RUN_DATE=datetime.utcnow().strftime("%Y%m%d")
RUN_TIME=datetime.utcnow().strftime("%H%M%S")

logging.basicConfig(level=logging.DEBUG)
opener = RedditUrlOpener() # Custom URL opener with user-agent string

# Download a snapshot of a comment thread
def download_snapshot(snapshot, attempt=0):
	json_url =  REDDIT_URL + snapshot.permalink + '.json'
	logging.debug("Opening " + json_url)
	u = opener.open(json_url)
	contents = u.read()
	u.close()
	if contents == '{"error": 304}':
		if attempt == 0:
			logging.info("Reddit has asked us to back off - sleeping for 30s")
			time.sleep(30)
			download_snapshot(snapshot,1)
		else:
			logging.error("Reddit has asked us to back off, we did, and it still won't give us the content. Moving on.")
	else:
		save_snapshot_comment(snapshot,contents)
	logging.debug("Sleeping 5 seconds to respect Reddit API rules")
	time.sleep(5)

# Save the comment to the appropriate file
def save_snapshot_comment(snapshot,json):
	snapshot_dir = get_snapshot_folder(snapshot);
	
	filename = snapshot_dir + "/" + snapshot.id + ".json"
	f = open(filename,'w')
	f.write(json)
	f.close()


# Construct the folder structure and return a location
def get_snapshot_folder(snapshot):
	base_dir = OUTPUT_DIR + '/' + snapshot.subreddit
	if not os.path.exists(base_dir):
		os.makedirs(base_dir)

	date_dir = base_dir + '/' + RUN_DATE
	if not os.path.exists(date_dir):
		os.makedirs(date_dir)		

	snapshot_dir = date_dir + '/' + RUN_TIME
	if not os.path.exists(snapshot_dir):
		os.makedirs(snapshot_dir)	

	return snapshot_dir

# Main

# CLI parser
#parser = argparse.ArgumentParser(description='Download useful stories associated with a Reddit JSON file')
#parser.add_argument('file')
#args = parser.parse_args()
#file = args.file

# Construct object

subreddits = {'programming','politics','malefashionadvice','atheism','unitedkingdom','apple','android','games','iphone'}

for subreddit in subreddits:

	ss = SubredditSnapshot(datetime.now())
	url = REDDIT_URL + "/r/" + subreddit + "/.json"
	logging.debug("Loading new subreddit from " + url)
	ss.load_from_url(url)
	logging.debug("Sleeping to respect Reddit API rules")
	time.sleep(5) 

	for snapshot in ss.stories:
		if snapshot.num_comments > 0:
			download_snapshot(snapshot)
		




