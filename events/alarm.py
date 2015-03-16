from threading import Thread
import logging


class Alarm:

	def __init__(self, weekday, hour, minute, action):
		self.setTime(weekday, hour, minute)
		self.setAction(action)
		self.active = False
		self.thread = None

	def parseField(self, value):
		if value == "*":
			return None
		return map(int, value.split(","))

	def setTime(self, weekday, hour, minute):
		self.weekdays = self.parseField(weekday)
		self.hours = self.parseField(hour)
		self.minutes = self.parseField(minute)

	def setAction(self, action):
		self.action = action

	def matchField(self, value, values):
		if values is None:
			return True
		for v in values:
			if v == value:
				return True
		return False

	def matchTime(self, dt):
		return self.matchField(dt.hour, self.hours) and \
		       self.matchField(dt.minute, self.minutes) and \
		       self.matchField(dt.weekday(), self.weekdays)

	def check(self, timeNow):
		match = self.matchTime(timeNow)
		if match:
			print("alarm match ", self.active, self.thread)
			if self.thread:
				print(self.thread.is_alive())
		if not match and self.active:
			self.active = False
		if match and not self.active:
			if self.thread is None:
				self.active = True
				self.thread = Thread(target=self.action)
				self.thread.start()
		if self.thread and not self.thread.is_alive():
			self.thread = None
			#self.active = False
