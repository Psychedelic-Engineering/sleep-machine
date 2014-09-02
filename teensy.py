import os
from serial import Serial, SerialException


class Teensy:

	def __init__(self):
		self.initialized = False
		try:
			self.initSerial()
			self.initialized = True
		except:
			pass

	def initSerial(self):
		try:
			for i in range(0, 5):
				devName = "/dev/ttyACM%d" % i
				if os.path.exists(devName):
					self.teensy = Serial(devName, 115200, timeout=10)
					return
			else:
				raise Exception("NoTeensy")
		except:
			raise Exception("NoTeensy")

	def write(self, strCommand):
		try:
			self.teensy.write(strCommand)
			response = self.teensy.readline().strip()
			return response
		except:
			pass