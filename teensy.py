import os, io, time, logging
from serial import Serial, SerialException


# Peripherie Factory
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
						logging.error("Error sending data")
						#raise
				except:
					logging.error("Error opening Serial")
					#raise
		logging.debug("Devices: %s", cls.devices)

	@classmethod
	def close(cls):
		for t in cls.devices:
			cls.devices[t].serial.close()


# Teensy Microcontroller
class Teensy:

	def __init__(self, device):
		self.initSerial(device)

	def __del__(self):
		if self.serial is not None:
			self.serial.close()
			logging.debug("Teensy close")

	def initSerial(self, device):
		self.serial = Serial(device, 115200, timeout=2)
		self.io = io.TextIOWrapper(io.BufferedRWPair(self.serial, self.serial))
		self.serial.flush()
		self.serial.flushInput()
		self.serial.flushOutput()
		time.sleep(0.5)

	def sendCommand(self, strCommand, seperator=None):
		# sende Kommando und liefere Ergebnis, besserer Name
		try:
			self.serial.flush()
			self.serial.write(strCommand)
			#self.serial.flush()
			response = self.serial.readline().strip()
			if seperator is not None:
				response = response.split(seperator)
			return response
		except:
			#raise
			return None

	def sendQuick(self, strCommand, seperator=None):
		# sende Kommando, besserer Name
		try:
			self.serial.flush()
			self.serial.write(strCommand)
			#self.serial.flush()
		except:
			#raise
			pass