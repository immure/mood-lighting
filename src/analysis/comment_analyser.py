import argparse
import json
import os
import logging
import re
import numpy
from time import sleep, ctime, gmtime,strftime, strptime, mktime
from datetime import *
from reddit.reddit_classes import *

logging.basicConfig(level=logging.DEBUG)

MIN_COMMENT_AGE=timedelta(minutes=0)
MAX_COMMENT_AGE=timedelta(minutes=50)

offset = datetime.now() - datetime.utcnow()

def load_page(filename,snapshot_time=None):
	f = open(filename,'r')
	j = json.load(f)
	post_age = ""
	f.close()
	comments = []
	for listing in j:
		data = listing['data']
		for child in data['children']:
			if child['kind'] == RedditConstants.KIND_POST:
				post_age = datetime.fromtimestamp(child['data']['created_utc'])
			if child['kind'] == RedditConstants.KIND_COMMENT:
				load_comments(child['data'], comments, snapshot_time=snapshot_time, post_age=post_age)
	return comments

def load_comments(comments_dict, comments_list, parent=None, snapshot_time=None, post_age=None):
	comment = RedditComment()
	comment.load_from_dict(comments_dict, parent, snapshot_time)

	include_comment = True

	# Edited comments mask scores, remove them

	if comment.edited:
		include_comment = False

	# We're only interested in analysing comments created up to 50 minutes
	# after the post
	delta = post_age - (comment.created_utc - offset)
	if delta < MIN_COMMENT_AGE or delta > MAX_COMMENT_AGE:
		include_comment = False

	if (include_comment):
		comments_list.append(comment)

	# Whether or not we're including the parent, check the children
	if (len(comments_dict['replies']) > 0):
		children = comments_dict['replies']['data']['children']
		for child in children:
			if child['kind'] == RedditConstants.KIND_COMMENT:
				load_comments(child['data'], comments_list, comment, snapshot_time, post_age)

# CLI parser
parser = argparse.ArgumentParser(description='Download useful stories associated with a Reddit JSON file')
parser.add_argument('folder')
args = parser.parse_args()
folder = args.folder

# Filename matcher

fnm = re.compile("[a-z0-9]*.json")

# Main

pages = []

dirList=os.listdir(folder)
for fname in dirList:
	if fnm.match(fname):
		# Get current time (as 'creation time')
		creation_time = datetime.fromtimestamp(os.path.getctime(folder + "/" + fname))
		creation_time = creation_time - offset
		pages.append(load_page(folder + fname, snapshot_time=creation_time))
	else:
		logging.warning('Unknown file: ' + fname)

tTime = os.path.split(os.path.dirname(folder))[1]
date = os.path.split(os.path.dirname(os.path.abspath(folder)))[1]

scores = []
times = []

for page in pages:
	for comment in page:
		scores.append(comment.score)
		times.append(comment.created_utc - offset)


scores.sort()
print "Number of comments: " + str(len(scores))
print "Max: " + str(max(scores))
print "Min: " + str(min(scores))
print "Mean: " + str(sum(scores)/len(scores))
print "Median: " + str(numpy.median(scores))
print "85th percentile: " + str(numpy.percentile(scores, 85))
print "15th percentile: " + str(numpy.percentile(scores, 15))
print "---"
print "Newest comment: " + str(max(times))
print "Oldest comment: " + str(min(times))


