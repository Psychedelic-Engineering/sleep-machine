
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

		skipLines = 20000
		for i in range(skipLines):
			self.line += 1
			response = self.file.readline()

	def initChannels(self):
		try:
			size = 20
			self.channels = []
			self.channels.append(Channel("TouchA", -200, 600, size))
			self.channels.append(Channel("TouchB", -200, 600, size))
			self.channels.append(Channel("TouchC", -200, 600, size))

			self.initialized = True
		except:
			print "initChannels error"
			self.initialized = False

	def readData(self):
		if not self.initialized:
			self.initChannels()
		for i in range(50):
			self.line += 1
			response = self.file.readline()

		try:
			values = map(float, response.split(","))

			self.channels[0].putValue(values[2])
			self.channels[1].putValue(values[3])
			self.channels[2].putValue(values[4])
		except:
			raise
			pass
