
from sensors import Sensor
from channel import Channel


class FakeSensor(Sensor):

	def __init__(self):
		self.initialized = False
		self.initChannels()
		self.line = 0
		self.openCSV("data/sleep.csv")

	def openCSV(self, filename):
		self.file = open(filename, 'r')
		response = self.file.readline()
		self.line += 1

		skipLines = 0
		for i in range(skipLines):
			self.line += 1
			response = self.file.readline()

	def initChannels(self):
		try:
			size = 60
			self.channels = []
			self.channels.append(Channel("Piezo", 0, 4096, size))
			self.channels.append(Channel("TouchA", 800, 2000, size))
			self.channels.append(Channel("TouchB", 800, 2000, size))
			self.channels.append(Channel("TouchC", 800, 2000, size))
			self.channels.append(Channel("AccelA", -5, 15, size))
			self.channels.append(Channel("AccelB", -5, 15, size))
			self.channels.append(Channel("AccelC", -5, 15, size))
			self.channels.append(Channel("GyroA", -5, 5, size))
			self.channels.append(Channel("GyroB", -5, 5, size))
			self.channels.append(Channel("GyroC", -5, 5, size))
			self.channels.append(Channel("Temp", 10, 30, size))
			self.initialized = True
		except:
			print "initChannels error"
			self.initialized = False

	def readData(self):
		if not self.initialized:
			self.initChannels()
		for i in range(1):
			self.line += 1
			response = self.file.readline()
		try:
			values = map(float, response.split(","))
			values = values[1:]
			for i, v in enumerate(values):
				self.channels[i].putValue(v)
		except:
			pass
			#raise
