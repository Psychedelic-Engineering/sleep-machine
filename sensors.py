from channel import Channel

"""
	Sensor Class
	ToDo:
	- ggf. abstrakte Klasse mit Sensor und Logfile als Unterklassen
	- oder "FromFile" Parameter
	- Logger integrieren?

	- initChannels und readData ggf. mit String-Parameter
		> kann von Sensor oder File-Reader kommen
"""


class Sensor:

	def __init__(self, device):
		self.initialized = False
		self.device = device
		self.initChannels()

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
		except:
			raise
