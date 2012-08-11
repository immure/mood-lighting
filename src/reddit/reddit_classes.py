import json
import logging
from datetime import *
from reddit.reddit_client import RedditUrlOpener

class SubredditSnapshot(object):

	"""A class representing a Subreddit snapshot"""
	def __init__(self, snapshot_time):
		super(SubredditSnapshot, self).__init__()
		self.snapshot_time = snapshot_time
		self.stories = []

	def snapshot_time(self):
		return self.snapshot_time

	def set_snapshot_time(self,snapshot_time_in):
		self.snapshot_time = snapshot_time_in

	def load_from_json(self,j):
		children = j['data']['children']
		for story in children:
			story_snapshot = RedditStorySnapshot()
			story_snapshot.load_from_dict(story['kind'],datetime.utcnow(),story['data'])
			self.stories.append(story_snapshot)

	def load_from_file(self,file):
		f = open(file,'r')
		j = json.load(f)
		f.close()
		self.load_from_json(j)

	def load_from_url(self, url):
		opener = RedditUrlOpener() # Custom URL opener with user-agent string
		u = opener.open(url)
		j = json.load(u)
		u.close()
		self.load_from_json(j)




	

class RedditStorySnapshot(object):

	"""A story (or link) on Reddit"""
	def __init__(self):
		super(RedditStorySnapshot, self).__init__()
		self.id = ""
		self.kind = ""
		self.domain = ""
		self.subreddit = ""
		self.title = ""
		self.author = ""
		self.created_utc = ""
		self.snapshot_utc = ""
		self.downs = ""
		self.ups = ""
		self.score = ""
		self.subreddit_id = ""
		self.url = ""
		self.permalink = ""
		self.num_comments = ""

	def load_from_dict(self, kind, snapshot_utc, dict):
		self.kind = kind
		self.id = dict['id']
		self.domain = dict['domain']
		self.subreddit = dict['subreddit']
		self.title = dict['title']
		self.author = dict['author']
		self.created_utc = dict['created_utc']
		self.snapshot_utc = snapshot_utc
		self.downs = dict['downs']
		self.ups = dict['ups']
		self.score = dict['score']
		self.subreddit_id = dict['subreddit_id']
		self.url = dict['url']
		self.permalink = dict['permalink']
		self.num_comments = dict['num_comments']



		