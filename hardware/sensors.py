import os
import time
import datetime
import logging
import gzip

from hardware.channel import Channel


"""
	Sensor Class
	- ggf. Logfile als Datasource per Parameter
	- Logging in eigene Klasse oder Scheduler
"""


class Sensor:

	def __init__(self, device):
		self.initialized = False
		self.device = device
		self.initSensor()
		self.logging = False
		self.buffer = ""
		self.lastTime = 0

	def initSensor(self):
		self.initialized = False
		try:
			header = self.device.sendCommand("?")
			header = header.split(";")
			logging.info("Initsensor: %s", header)
			self.initChannels(header)
			self.device.write("b 0")
			self.device.write("l 0")
		except:
			raise
			logging.error("Initsensor error")

	def initChannels(self, header):
		self.channels = []
		for sensor in header:
			if sensor != "":
				name, params = sensor.split(":")
				num, min, max = params.split(",")
				num = int(num)
				min, max = float(min), float(max)
				for i in range(num):
					self.channels.append(Channel(name, min, max, 100))
		self.initialized = True

	def readData(self):
		if not self.initialized:
			self.initSensor()
		values = None
		try:
			values = self.device.sendCommand("!", ",")
			if values and len(values) == len(self.channels):
				values = map(float, values)
				self.logData(values)
				for i, v in enumerate(values):
					self.channels[i].putValue(v)
		except:
			pass

	def readRaw(self):
		now = int(10*time.time())
		if now > self.lastTime:
			#data = self.device.readWaiting()
			self.lastTime = now
			data = self.device.sendCommand("!")
			self.buffer += str(now) + "," + data + "\n"
			if len(self.buffer) >= 20000:
				logging.info("Writing Buffer")
				file = gzip.open('logfile.txt.gz', 'a')
				#file = open("logfile.txt", "a")
				file.write(self.buffer)
				file.close()
				self.buffer = ""

	def calibrate(self):
		for c in self.channels:
			c.calibrate()

	# logging, ggf. in eigene Klasse
	def startLogging(self):
		logging.debug("startLogging")
		self.logging = True
		self.logDate = datetime.date.today()
		self.logFile = self.logDate.strftime("data/%Y-%m-%d.csv")

	def stopLogging(self):
		logging.debug("stopLogging")
		self.logging = False

	def logData(self, values):
		if self.logging:
			fileExists = os.path.isfile(self.logFile)
			timestamp = time.time()
			file = open(self.logFile, "a")
			if not fileExists:
				names = [c.name for c in self.channels]
				file.write("time," + ','.join(names) + "\n")
			file.write(str(timestamp) + "," + ','.join(map(str, values)) + "\n")
			file.close()


