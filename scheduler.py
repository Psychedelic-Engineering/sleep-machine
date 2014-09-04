from astral import Location
import datetime, time
import pytz

"""
	Scheduler
	- Events
	- Phasen & States
	- Aktionen (Logging, Processing,
"""

class Scheduler:

	def __init__(self):
		self.lastTime = time.time()
		self.startTime = self.lastTime
		self.counter = 0

	def check(self):
		pass

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
		if (self.counter % 20) == 0:
			self.fps = 20 / (now - self.startTime)
			self.startTime = now
			print self.fps

	def getSunTimes(self):
		a = Location()
		a.timezone = "Europe/Berlin"
		tz = pytz.timezone(a.timezone)

		first = datetime.date(2014,1,1)
		for day in range(365):
			date = first + datetime.timedelta(days=day)
			sunData = a.sun(date)
			print date.strftime("%Y-%m-%d")
			print sunData['sunrise'].time(), sunData['sunset'].time()

		print a.sun(datetime.date.today())
		"""
		#lets get the sunset and sunrise times
		a_sunset = a.sunset()
		a_sunrise = a.sunrise()

		#lets get current time and localize it
		n = datetime.datetime.now()
		n = tz.localize(n)

		#some debugging
		logging.debug("NOW: %s; sunrise: %s; dif: %s"  % (n, a_sunrise, n - a_sunrise))
		logging.debug("NOW: %s; sunset: %s; dif: %s" % (n, a_sunset, n - a_sunset))
		"""



def parseTime(strTime):
	return datetime.strptime(strTime, "%H:%M")


def dayTime(dt):
	return replaceDate(dt, date.min)


def replaceDate(dt, newDate=None):
	if newDate is None:
		newDate = datetime.now().date()
	return datetime.combine(newDate, dt.time())


class Alarm:
	time = ""
	periodic = False
	over = False
	action = None

	def __init__(self, timeStr, action, periodic=False):
		self.time = dayTime(parseTime(timeStr))
		self.periodic = periodic
		self.action = action
		self.over = False
		self.thread = None
		self.state = "pending"

	def check(self, timeNow):
		diff = int((self.time - timeNow).total_seconds())
		if 0 > diff and self.state == "pending":
			self.state = "active"
			self.thread = Thread(target=self.action, args=(self.finished,))
			self.thread.start()
		elif self.state == "active":
			pass
		if self.thread:
			if not self.thread.is_alive():
				self.state = "done"
		return diff

	def finished(self):
		print "callback"
		if self.periodic and self.over:
			print "over"
			self.over = False

	def getTimeStr(self):
		return replaceDate(self.time).strftime("%H:%M")




class Alarmclock:
	alarms = []

	def add(self, timeStr, action, periodic=False):
		newAlarm = Alarm(timeStr, action, periodic)
		self.alarms.append(newAlarm)

	def check(self, now):
		timeNow = dayTime(now)
		for alarm in self.alarms:
			result = alarm.check(timeNow)
			#print str(result) + " - " + str(alarm.over)
