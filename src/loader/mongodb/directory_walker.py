import os

# Directory structure:
#
# subreddit/date/time/*.json

class DirectoryWalker():

	def __init__(self, initial_dir, queue):
		self.initial_dir = initial_dir

		self.file_count=self.count_files()
		self.file_number=0

	def count_files(self):
		count = 0
		for dirname, dirnames, filenames in os.walk(self.initial_dir):
			for filename in filenames:
		 		count += 1
		return count

	def start(self):
		for dirname, dirnames, filenames in os.walk(self.initial_dir):
			for filename in filenames:
		 		queue.put(filename)

