import os, io, time
from serial import Serial, SerialException


class Peripherals:

	devices = {}

	@classmethod
	def init(cls):
		devPath = "/dev/"
		teensyBaseMac = "tty.usbmodem"
		teensyBaseRaspi = "ttyACM"

		for file in os.listdir(devPath):

			if file.startswith(teensyBaseMac) or file.startswith(teensyBaseRaspi):
				device = devPath + file
				try:
					teensy = Teensy(device)
					try:
						response = teensy.sendCommand("i", seperator="|")
						deviceName = response[0]
						if deviceName != "":
							cls.devices[response[0]] = teensy
					except:
						print "Error sending data"
						#raise
				except:
					print "Error opening Serial"
					#raise
		print cls.devices


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
		self.serial.flush()
		time.sleep(0.5)

	def sendCommand(self, strCommand, seperator=None):
		try:
			self.serial.flush()
			self.serial.write((strCommand))
			self.serial.flush()
			response = self.serial.readline().strip()
			if seperator is not None:
				response = response.split(seperator)
			return response
		except:
			#raise
			return None