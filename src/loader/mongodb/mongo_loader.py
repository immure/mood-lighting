from loader.mongodb.mongo_worker import MongoSaver
from loader.mongodb.console_output import LoaderConsoleOutput
from loader.mongodb.program_state import ProgramState
from loader.mongodb.model import RedditComment
from loader.mongodb.model import CommentSaver

import pymongo
import json
import logging
import os
import sys
import re
import string
import Queue


from datetime import datetime

# Set up MongoDB connections

connection = pymongo.Connection()

db = connection.posts

sample_file='sample.json'

loaded = 0
currentFile = ''

comments_db = db.comments
words_db = db.words

# Load stoplist into memory

for line in open('loader/stoplist.txt','r'):
	stopwords = re.findall(r"\b[a-z]+\b", line, re.I)

# Initiate the program control object

state = ProgramState()

# Initiate the Save queues

comment_saver = MongoSaver(5,comments_db,state)
word_saver = MongoSaver(25,words_db,state)

# Initiate the console outputter

output = LoaderConsoleOutput(comment_saver, word_saver, state)
output.start()

# Create the saver

saver = CommentSaver(stopwords,comment_saver,word_saver)




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

try:
	dir="../data/data/"

	fileCount = 0
	fileNumber = 0

	for community_folder in os.listdir(dir):
		for date_folder in os.listdir(dir + community_folder):
			for time_folder in os.listdir(dir + community_folder + '/' + date_folder):
				for name in os.listdir(dir + community_folder + '/' + date_folder + '/' + time_folder):
					fileCount = fileCount + 1

	#print "{0} files to process..".format(str(fileCount))
	output.set_target_files(str(fileCount))

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
							#try:
								
							saver.save(rc)
							output.set_processed_files(fileNumber)
							#if loaded % 2500 == 0:
							#	print "{0} Saved file number {1} of {2} - {3}% ({4})".format(datetime.now().strftime("%H:%M:%S"),
							#		str(fileNumber),str(fileCount),str(round((float(fileNumber)/fileCount)*100)),currentFile)
								#print "Comments DB size: {0}".format(comments_db.count())
								#print "Words DB size: {0}".format(words_db.count())
					except (KeyboardInterrupt, SystemExit):
						raise
					except:
						print "Unable to parse {0}".format(full_path)
						print "Unexpected error:", sys.exc_info()[0]
						raise
except (KeyboardInterrupt, SystemExit):
	state.stop()
	print "Caught interrupt, closing down"
except:
	state.stop()
	raise