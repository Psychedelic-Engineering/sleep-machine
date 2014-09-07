import datetime
from utilities.date import *
from threading import Thread

class Alarm:

	def __init__(self, timeStr, action, periodic=False):
		self.time = dayTime(parseTime(timeStr))
		self.periodic = periodic
		self.action = action
		self.over = False
		self.thread = None
		self.state = "pending"

	def check(self, timeNow):
		timeNow = dayTime(timeNow)
		diff = int((self.time - timeNow).total_seconds())
		if 0 > diff and self.state == "pending":
			self.state = "active"
			#self.thread = Thread(target=self.action, args=(self.finished,))
			self.thread = Thread(target=self.action)
			self.thread.start()
		elif self.state == "active":
			pass
		if self.thread:
			if self.state == "active" and not self.thread.is_alive():
				#print "Thread finished"
				self.state = "done"
		return diff

	def finished(self):
		#print "callback"
		if self.periodic and self.over:
			self.over = False
	"""
	def getTimeStr(self):
		return replaceDate(self.time).strftime("%H:%M")
	"""