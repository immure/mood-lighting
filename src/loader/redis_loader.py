import json
import logging
import os
import sys
import re
import string
import load_stoplist
from time import sleep
from threading import Thread
from redis import Redis
from redis.exceptions import ConnectionError

loaded = 0
currentThreads = 0
blockedThreads = 0
currentFile = ''

r=Redis()
r.flushdb()
load_stoplist.load_stoplist()

class RedditComment:
	def __init__(self,j):
		#print json.dumps(j,sort_keys=True, indent=4)
		self.author 	= j['author']
		self.comment 	= j['body']
		self.id 		= j['id']
		self.score 		= j['ups']-j['downs']
		self.community 	= j['subreddit']
		self.created_utc = j['created_utc']

	def save(self):
		global r
		if not r.exists(self.id):
			RedditCommentSaver(self)
		global loaded 
		loaded = (loaded + 1)

	def print_info(self):
		print self.community + " " + self.id + " " + self.author + " " + str(self.score)

class RedditCommentSaver(Thread):
	def __init__(self,rc):
		#Thread.__init__(self)
		self.rc = rc
		global currentThreads
		global blockedThreads
		currentThreads = currentThreads + 1
		#print "currentThreads = {0} blockedThreads = {1}".format(currentThreads,blockedThreads)
		while (currentThreads > 150):
			blockedThreads = blockedThreads + 1
			sleep(1)
			blockedThreads = blockedThreads - 1
		#self.start()
		self.run()

	def run(self):
		global r
		if not r.exists(rc.id):
			r.set(rc.id,{rc.author,rc.comment,rc.id,rc.score,rc.community,rc.created_utc})
			r.sadd('authors',rc.author);
			r.lpush(rc.author + '_scores', rc.score)
			r.sadd(rc.author + '_comments', rc.id)
			r.sadd(rc.community + '_comments', rc.id)
			r.zincrby('zauthor_' + rc.community, rc.author, rc.score)
			r.zincrby('zauthorglobal', rc.author, rc.score)

			words = re.findall(r"\b[a-z]+\b", string.lower(rc.comment), re.I)
			for word in words:
				if not r.sismember('stoplist',word):
					r.sadd('words',word)
					r.sadd('words_' + rc.community, word)
					r.lpush('wordglobal_' + word, rc.score)
					r.zincrby('zword_' + rc.community, word, rc.score)
					r.zincrby('zwordglobal', word, rc.score)
					r.lpush('word_' + rc.community + '_' + word + '_scores', rc.score)
					r.sadd(word + '_comments', rc.id)
			global currentThreads
			currentThreads = currentThreads - 1



def add_comments_to_list(j,l):

	# Is a comment
	try:

		rc = RedditComment(j['data'])
		l.append(rc)

		if 'replies' in j['data'] and 'data' in j['data']['replies']:
			for child in j['data']['replies']['data']['children']:
				if child['kind'] == 't1':
					add_comments_to_list(child,l)
	except:
		print "Unexpected error:", sys.exc_info()[0]




my_file="../../data/data/Android/20120811/132734/xzobx.json"

dir="../../data/data/"

fileCount = 0
fileNumber = 0

for community_folder in os.listdir(dir):
	for date_folder in os.listdir(dir + community_folder):
		for time_folder in os.listdir(dir + community_folder + '/' + date_folder):
			for name in os.listdir(dir + community_folder + '/' + date_folder + '/' + time_folder):
				fileCount = fileCount + 1

print "{0} files to process..".format(str(fileCount))

for community_folder in os.listdir(dir):
	for date_folder in os.listdir(dir + community_folder):
		for time_folder in os.listdir(dir + community_folder + '/' + date_folder):
			for name in os.listdir(dir + community_folder + '/' + date_folder + '/' + time_folder):
				full_path = dir + community_folder + '/' + date_folder + '/' + time_folder + '/' + name
				currentFile = full_path
				fileNumber = fileNumber + 1

				try:
					j = json.load(open(full_path,'r'))
					l = []

					for listing in j:
						for child in listing['data']['children']:
							if child['kind'] == "t1":
								add_comments_to_list(child,l)

					for rc in l:
						try:
							rc.save()
						except ConnectionError as e:
							print "Redis Connection error, retrying: {0}".format(e)
							try:
								rc.save()
							except ConnectionError as e:
								print "Redis connection error again - aborting: {0}".format(e)
						if loaded % 2500 == 0:
							print "Saved file number {0} of {1} - {2}% ({3})".format(
								str(fileNumber),str(fileCount),str(round((float(fileNumber)/fileCount)*100)),currentFile)
				except:
					print "Unable to parse {0}".format(full_path)




