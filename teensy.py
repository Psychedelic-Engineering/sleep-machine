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
					teensy = Teensy(device)
					try:
						response = teensy.sendCommand("i", seperator="|")
						cls.devices[response[0]] = teensy
					except:
						print "Error sending data"
						#raise
				except:
					print "Error opening Serial"
					#raise



class Teensy:

	def __init__(self, device):
		self.initSerial(device)

	def __del__(self):
		if self.serial is not None:
			self.serial.close()
			print "Teensy close"

	def initSerial(self, device):
		self.serial = Serial(device, 115200, timeout=0.1)
		self.io = io.TextIOWrapper(io.BufferedRWPair(self.serial, self.serial))
		self.io.flush()
		time.sleep(0.2)

	def sendCommand(self, strCommand, seperator=None):
		try:
			self.io.write(unicode(strCommand))
			self.io.flush()
			response = self.io.readline().strip()
			print "Resp: ", response
			if seperator is not None:
				response = response.split(seperator)
			return response
		except:
			return None