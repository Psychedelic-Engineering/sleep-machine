from astral import Location
from datetime import datetime, date
import time, logging, pytz
from events.alarm import Alarm
from utilities.date import *

"""
	Scheduler
"""

class Scheduler:

	def __init__(self):
		self.lastTime = time.time()
		self.startTime = self.lastTime
		self.counter = 0
		self.alarms = []

	def addAlarm(self, weekday, hour, minute, action):
		newAlarm = Alarm(weekday, hour, minute, action)
		self.alarms.append(newAlarm)

	def checkAlarm(self):
		timeNow = datetime.now()
		for alarm in self.alarms:
			alarm.check(timeNow)

	def elapsed(self, seconds):
		now = time.time()
		elapsed = now - self.lastTime
		if elapsed > seconds:
			self.lastTime = now
			self.getFPS(now)
			return True
		else:
			return False

	def getFPS(self, now):
		self.counter += 1
		if (self.counter % 100) == 0:
			self.fps = 100.0 / (now - self.startTime)
			self.startTime = now
			logging.debug("%.2f fps", self.fps)

	def getSunTimes(self):
		a = Location()
		a.timezone = "Europe/Berlin"
		tz = pytz.timezone(a.timezone)
		sunData = a.sun()
		n = datetime.datetime.now()
		n = tz.localize(n)

