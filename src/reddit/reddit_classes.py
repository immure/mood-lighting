import json

class SubredditSnapshot(object):

	"""A class representing a Subreddit snapshot"""
	def __init__(self, snapshot_time):
		super(SubredditSnapshot, self).__init__()
		self.snapshot_time = snapshot_time

	def snapshot_time(self):
		return self.snapshot_time

	def set_snapshot_time(self,snapshot_time_in):
		self.snapshot_time = snapshot_time_in

	def load_from_file(self,file):
		f = open(file,'r')
		j = json.load(f)
		f.close()
		print json.dumps(j, sort_keys=True, indent=4)



	

class RedditStorySnapshot(object):
	"""A story (or link) on Reddit"""
	def __init__(self, arg):
		super(RedditStorySnapshot, self).__init__()
		self.arg = arg

	def title(self):
		return self.title

	def set_title(self,title_in):
		self.title = title_in
		