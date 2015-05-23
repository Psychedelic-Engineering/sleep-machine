import os, io, time, logging
from serial import Serial, SerialException


# Peripherie Factory
class Peripherals:
	devices = {}
	knownDevices = ("Basestation", "Pillow")

	@classmethod
	def init(cls):
		devPath = "/dev/"
		teensyBaseMac = "tty.usbmodem"
		teensyBaseRaspi = "ttyACM"
		for fileName in os.listdir(devPath):
			if fileName.startswith(teensyBaseMac) or fileName.startswith(teensyBaseRaspi):
				devName = devPath + fileName
				try:
					teensy = Teensy(devName)
					print teensy
					if teensy.name in cls.knownDevices:
						cls.devices[teensy.name] = teensy
				except:
					logging.error("Error opening Serial")
					#raise
		logging.info("Devices: %s", cls.devices)

	@classmethod
	def reInit(cls):
		pass

	@classmethod
	def close(cls):
		for t in cls.devices:
			cls.devices[t].serial.close()


# Teensy Microcontroller
class Teensy:

	def __init__(self, device):
		self.errorCount = 0
		self.initSerial(device)

	def __del__(self):
		if self.serial is not None:
			self.serial.close()
			#logging.debug("Teensy close")

	def initSerial(self, device):
		self.serial = Serial(device, 115200, timeout=1)
		self.serial.write("l 0")
		self.serial.flushInput()
		self.initDevice()

	def initDevice(self):
		response = self.sendCommand("i", seperator="|")
		self.name = None
		try:
			name = response[0]
			if name:
				self.name = name
		except:
			print "InitDevice Error"
			pass

	def write(self, data):
		self.serial.write(data)

	def read(self, numBytes):
		return self.serial.read(numBytes)

	def readWaiting(self):
		if self.serial.inWaiting() > 0:
			return self.read(self.serial.inWaiting())
		return ""

	def sendCommand(self, strCommand, seperator=None):
		# sende Kommando und liefere Ergebnis, besserer Name
		try:
			#self.serial.flush()
			self.serial.write(strCommand)
			#self.serial.flush()
			response = self.serial.readline().strip()
			if seperator is not None:
				response = response.split(seperator)
			return response
		except SerialException as e:
			print "Error sendCommand", type(e), e.message
			self.reCover()
			raise
			# device reports readiness to read but returned no data (device disconnected or multiple access on port?)
			# Attempting to use a port that is not open
			# write failed: [Errno 6] Device not configured

	def reCover(self):
		self.errorCount += 1
		if self.errorCount > 10:
			self.serial.close()
			print "Reinit Serial"
			self.initSerial(self.serial.name)
			self.serial.flush()
			self.errorCount = 0
			time.sleep(1)

	def sendQuick(self, strCommand):
		# sende Kommando, besserer Name
		try:
			self.serial.flush()
			self.serial.write(strCommand)
			#self.serial.flush()
		except:
			raise