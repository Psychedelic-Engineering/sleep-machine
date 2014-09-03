import os.path

class Logger:

	def __init__(self, sensor):
		self.sensor = sensor
		self.names = [c.name for c in sensor.channels]
		self.logfile = "logfile.txt"

	def writeHeader(self):
		self.file = open(self.logfile, "a")
		self.file.write("time," + ','.join(self.names) + "\n")
		self.file.close()

	def write(self, time, values):
		if not os.path.isfile(self.logfile):
			self.writeHeader()
		self.file = open(self.logfile, "a")
		self.file.write(str(time) + "," + ','.join(map(str, values))+"\n")
		self.file.close()

	def __del__(self):
		print "EXIT"