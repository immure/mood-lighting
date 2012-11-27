from threading import Thread
import Queue

class MongoSaveWorker(Thread):
	def __init__(self, queue, db, state):
		self.__queue__ = queue
		self.__db__ = db
		self.__state__ = state
		Thread.__init__(self)

	def run(self):
		self.__state__.register(self)
		while self.__state__.is_running():
			try:
				item = self.__queue__.get(True, 1)
				if item is None:
					print "got nothing!"
					break
				try:
					self.__db__.insert(item)
				except:
					print "DB insert error for: {0}".format(item)
			except Queue.Empty:
				None
		self.__state__.unregister(self)

class MongoSaver():
	def __init__(self, num_workers, db, state):

		self.__q__ = Queue.Queue(num_workers * 3)
		self.__db__ = db
		self.__state__ = state

		for i in range(num_workers):
			worker = MongoSaveWorker(self.__q__, db, state)
			worker.start()

	def save(self,item):
		self.__q__.put(item)

	def backlog_size(self):
		return self.__q__.qsize()

	def put(self,item):
		self.save(item)

	def qsize(self):
		return self.backlog_size()

	def exists(self,query):
		return self.__db__.find_one(query) is not None

