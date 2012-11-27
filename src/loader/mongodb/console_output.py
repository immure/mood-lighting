from threading import Thread
from sys import stdout
from time import sleep

class LoaderConsoleOutput(Thread):
	def __init__(self, comments_queue, words_queue, state):
		self.__processed_files__ = 0
		self.__target_files__ = 0
		self.__state__ = state
		self.__words_queue__ = words_queue
		self.__comments_queue__ = comments_queue
		Thread.__init__(self)

	def set_processed_files(self, processed_files):
		self.__processed_files__ = processed_files

	def set_target_files(self, target_files):
		self.__target_files__ = target_files

	def run(self):
		while self.__state__.is_running():
			try:
				percent = 0
				if (self.__target_files__ > 0):
					percent = round((float(self.__processed_files__)/float(self.__target_files__))*100,1)
				stdout.write("\r{0}/{1} {2}% Threads: {3} Comment queue: {4} Word queue: {5}                               ".format(
					self.__processed_files__, self.__target_files__, 
					percent, self.__state__.num_threads(), self.__comments_queue__.qsize(), 
					self.__words_queue__.qsize()))
				stdout.flush()
				sleep(1)
			except:
				self.__state__.stop()
				raise