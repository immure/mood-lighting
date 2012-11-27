import re
import string

class RedditComment:
	def __init__(self,j):
		#print json.dumps(j,sort_keys=True, indent=4)
		self.author 	= j['author']
		self.comment 	= j['body']
		self.id 		= j['id']
		self.score 		= j['ups']-j['downs']
		self.community 	= j['subreddit']
		self.created_utc = j['created_utc']

	def save(self, comments_db,words_db,comments_save_queue,words_save_queue):
		if not comments_db.find_one({"id":rc.id}):
			RedditCommentSaver(self,comments_db,words_db,comments_save_queue,words_save_queue)

	def print_info(self):
		print self.community + " " + self.id + " " + self.author + " " + str(self.score)

# Translation functions		

def expand_word_list(comment):
	return re.findall(r"\b[a-z]+\b", string.lower(comment.comment), re.I)

def word_to_dict(word, comment):
	return {"word":word, "community":comment.community, "score": comment.score}

def comment_to_dict(comment):
	return {"id":comment.id,"author":comment.author,"comment":comment.comment,
		"score":comment.score,"community":comment.community,"created_utc":comment.created_utc}

# Saver

class CommentSaver:

	def __init__(self, stoplist, comment_saver, word_saver):
		self.__stoplist__ = stoplist
		self.__cs__ = comment_saver
		self.__ws__ = word_saver
	
	def save(self, comment):
		if not self.__cs__.exists(comment.id):
			self.__save_comment(comment_to_dict(comment))
			words = expand_word_list(comment)

	def __save_words(self, words):
		for word in words:
			if not word in self.__stoplist__:
				self.__save_word(word_to_dict(word,comment))

	def __save_word(self, word_dict):
		self__ws__.save(word_dict)

	def __save_comment(self, comment_dict):
		self.__cs__.save(comment_dict)




# class RedditCommentSaver():
# 	def __init__(self,rc,comments_db,words_db,comments_save_queue, words_save_queue):
# 		self.rc = rc
# 		self.__comments_db__ = comments_db
# 		self.__words_db__ = words_db
# 		self.__comments_save_queue__ = comments_save_queue
# 		self.__words_save_queue__ = words_save_queue
# 		self.run()

# 	def run(self):


# 		if not self.__comments_db__.find_one({"id":self.rc.id}):
# 			self.__comments_save_queue__.put({"id":self.rc.id,"author":self.rc.author,"comment":self.rc.comment,
# 				"score":self.rc.score,"community":self.rc.community,"created_utc":self.rc.created_utc})
# 			#r.lpush(rc.author + '_scores', rc.score)
# 			#r.sadd(rc.author + '_comments', rc.id)
# 			#r.sadd(rc.community + '_comments', rc.id)
# 			#r.zincrby('zauthor_' + rc.community, rc.author, rc.score)
# 			#r.zincrby('zauthorglobal', rc.author, rc.score)

# 			words = re.findall(r"\b[a-z]+\b", string.lower(self.rc.comment), re.I)
# 			for word in words:
# 				global stopwords
# 				if not word in stopwords:
# 					self.__words_save_queue__.put({"word":word, "community":self.rc.community, "score": self.rc.score})