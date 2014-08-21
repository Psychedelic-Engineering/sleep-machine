import os
from serial import Serial, SerialException
from channel import Channel
import numpy

class Sensor:

	def __init__(self):
		self.initialized = False
		self.initSerial()
		self.initChannels()

	def initSerial(self):
		try:
			devName = "/dev/cu.usbmodem228731"
			if os.path.exists(devName):
				self.teensy = Serial(devName, 115200, timeout=0.1)
				return
			else:
				raise Exception("NoTeensy")
		except:
			raise Exception("NoTeensy")

	def checkTeensy(self):
		self.teensy.write("i")
		response = self.teensy.readline().strip()
		print "init sensors: %s" % response
		return response == "ok"

	def initChannels(self):
		self.checkTeensy()
		try:
			self.channels = []
			self.teensy.write("?")
			response = self.teensy.readline().strip()
			sensors = response.split(";")

			for sensor in sensors:
				if sensor != "":
					name, params = sensor.split(":")
					num, min, max = params.split(",")
					num = int(num)
					min, max = float(min), float(max)
					for i in range(num):
						self.channels.append(Channel(name, min, max, 10))
			self.channels[1].min = -400
			self.channels[1].max = 400
			#self.channels[1].offset = -1014
			self.channels[2].min = -400
			self.channels[2].max = 400
			#self.channels[2].offset = -1222
			self.channels[3].min = -400
			self.channels[3].max = 400
			#self.channels[3].offset = -1148

			self.initialized = True
			print self.initialized

			print self.channels
		except:
			print "initChannels error"
			self.initialized = False

	def readData(self):
		if not self.initialized:
			self.initChannels()
		self.teensy.write("!")
		response = self.teensy.readline().strip()
		#print response
		try:
			values = map(float, response.split(","))
			for i, v in enumerate(values):
				self.channels[i].putValue(v)
		except:
			self.initialized = False

	def getValues(self):
		res = []
		for i in self.channels:
			res.append(i.getValue())
		return res

	def getAvgs(self):
		res = []
		for i in self.channels:
			res.append(i.getBufferAvg())
		return res

	def getTotalAvgs(self):
		res = []
		for i in self.channels:
			res.append(i.getAvg())
		return res

	def getDerivs(self):
		res = []
		for i in self.channels:
			res.append(i.getDeriv())
		return res

	def getRanges(self):
		res = []
		for i in self.channels:
			res.append(i.getRng())
		return res
