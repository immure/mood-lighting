class ProgramState:
	def __init__(self):
		self.__running__ = True
		self.__num_threads__ = 0

	def stop(self):
		print "Sent kill signal to all threads"
		self.__running__ = False

	def is_running(self):
		return self.__running__

	def register(self,thread):
		self.__num_threads__ = self.__num_threads__ + 1

	def unregister(self,thread):
		self.__num_threads__ = self.__num_threads__ - 1

	def num_threads(self):
		return self.__num_threads__