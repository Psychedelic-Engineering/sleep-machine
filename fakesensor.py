
from sensors import Sensor
from channel import Channel


class FakeSensor(Sensor):

	def __init__(self):
		self.initialized = False
		self.initChannels()
		self.line = 0
		self.openCSV("sleep.csv")

	def openCSV(self, filename):
		self.file = open(filename, 'r')
		response = self.file.readline()
		self.line += 1

	def initChannels(self):
		try:
			size = 40
			self.channels = []
			self.channels.append(Channel("TouchA", -100, 600, size))
			self.channels.append(Channel("TouchB", -100, 600, size))
			self.channels.append(Channel("TouchC", -100, 600, size))

			self.initialized = True

			print self.channels
		except:
			print "initChannels error"
			self.initialized = False

	def readData(self):
		if not self.initialized:
			self.initChannels()
		for i in range(1):
			self.line += 1
			response = self.file.readline()
		#response = self.file.readline()
		try:
			values = map(float, response.split(","))

			self.channels[0].putValue(values[2])
			self.channels[1].putValue(values[3])
			self.channels[2].putValue(values[4])
		except:
			print self.line
			#raise
			pass
