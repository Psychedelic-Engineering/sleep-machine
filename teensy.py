import os, io, time
from serial import Serial, SerialException


class Peripherals:

	devices = {}

	@classmethod
	def init(cls):
		devPath = "/dev/"
		teensyBaseName = "tty.usbmodem"
		teensyBaseName = "ttyACM"

		for file in os.listdir(devPath):

			if file.startswith(teensyBaseName):
				device = devPath + file
				try:
					serial = Serial(device, 115200, timeout=1)
					print serial.name
					teensy = Teensy(serial)
					try:
						response = teensy.sendCommand("i", seperator="|")
						cls.devices[response[0]] = teensy
						time.sleep(1)
					except:
						print "Error sending data"
						#raise
				except:
					print "Error opening Serial"
					#raise



class Teensy:

	def __init__(self, serial):
		self.serial = serial
		self.io = io.TextIOWrapper(io.BufferedRWPair(serial, serial))

	def sendCommand(self, strCommand, seperator=None):
		try:
			self.io.flush()
			self.io.write(unicode(strCommand))
			self.io.flush()
			response = self.io.readline().strip()
			if seperator is not None:
				response = response.split(seperator)
			return response
		except:
			return None