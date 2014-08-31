import os
from serial import Serial, SerialException
from channel import Channel

class Sensor:

	def __init__(self):
		self.initialized = False
		self.initSerial()
		self.initChannels()

	def __del__(self):
		print "Close Teensy"
		self.teensy.close()

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
		print "Init Teensy: %s" % response
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

			self.initialized = True
		except:
			print "initChannels error"
			self.initialized = False

	def readData(self):
		if not self.initialized:
			self.initChannels()
		self.teensy.write("!")
		response = self.teensy.readline().strip()

		try:
			values = map(float, response.split(","))
			for i, v in enumerate(values):
				self.channels[i].putValue(v)
		except:
			raise
			self.initialized = False
