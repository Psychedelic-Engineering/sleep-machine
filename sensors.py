from channel import Channel

"""
	Sensor Class
	ToDo:
	- ggf. abstrakte Klasse mit Sensor und Logfile als Unterklassen
	- oder "FromFile" Parameter
	- Logger integrieren?

	- Datasource: Init, getInfo, readData (Logfile, Teensy)
	- Sensor: setDataSource, initChannels, readData, setLogging
"""


class Sensor:

	def __init__(self, device):
		self.initialized = False
		self.device = device
		self.initChannels()
		self.minV = 100000
		self.maxV = 0

	def stats(self):
		print "minmax: ", self.minV, self.maxV

	def initChannels(self):
		try:
			self.channels = []
			sensors = self.device.sendCommand("?", ";")
			print "initChannels: ", sensors

			for sensor in sensors:
				if sensor != "":
					name, params = sensor.split(":")
					num, min, max = params.split(",")
					num = int(num)
					min, max = float(min), float(max)
					for i in range(num):
						self.channels.append(Channel(name, min, max, 100))
			self.initialized = True
		except:
			print "initChannels error"
			self.initialized = False

	def readData(self):
		if not self.initialized:
			self.initChannels()

		try:
			values = self.device.sendCommand("!", ",")
			values = map(float, values)
			for i, v in enumerate(values):
				self.channels[i].putValue(v)
				if i in (1,2,3):
					self.minV = min(self.minV, v)
					self.maxV = max(self.maxV, v)
		except:
			raise
