from redis import Redis
import re
import string


def load_stoplist():
	r = Redis()
	for line in open('stoplist.txt','r'):
		words = re.findall(r"\b[a-z]+\b", line, re.I)
		for word in words:
			r.sadd('stoplist',string.lower(word))