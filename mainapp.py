import time, logging, sys
from display.display import Display
from fakesensor import FakeSensor
from sensors import Sensor
from display.graph import Graph
from display.clock import Clock
from teensy import Peripherals
from scheduler import Scheduler
import pygame
from basestation import LED


class SleepApp:

	def __init__(self):
		self.isRaspberry = False
		self.emulateSensor = False
		logging.basicConfig(format='%(message)s', level=logging.DEBUG)
		logging.debug("init app")
		self.quitting = False
		Peripherals.init()
		screenMult = 1
		if self.emulateSensor:
			self.sensor = FakeSensor()
		else:
			self.sensor = Sensor(Peripherals.devices["Pillow"])
		self.led = LED(Peripherals.devices["Basestation"])
		self.display = Display(screenMult*320, screenMult*240, self.isRaspberry)
		self.graph = Graph(self.display, self.sensor)
		self.clock = Clock(self.display)
		self.scheduler = Scheduler()
		#self.sensor.startLogging()

		#self.scheduler.addAlarm("*", "*", "0,5,10,15,20,25,30,35,40,45,50,55", self.doAlarm)
		self.scheduler.addAlarm("*", "*", "21", self.sensor.startLogging)
		self.scheduler.addAlarm("*", "*", "22", self.sensor.stopLogging)
		self.scheduler.addAlarm("*", "*", "*", self.doAlarm)
		#self.doAlarm()
		#self.quit()

	def start(self):
		logging.debug("start app")
		while True:
			if self.scheduler.elapsed(0.1):
				self.sensor.readData()
				self.clock.render()
				self.graph.render()
				self.scheduler.checkAlarm()

				for event in pygame.event.get():
					if event.type == pygame.MOUSEBUTTONDOWN:
						print event
						pass

	def quit(self):
		logging.debug("Quit app")
		Peripherals.close()
		self.quitting = True
		time.sleep(1)
		sys.exit()

	def doAlarm(self):

		off = 1.0
		on = 0.001
		lum = 1.0
		while off >= 0.1:
			print off, on, lum
			for i in range(5):
				self.led.setLum(lum, lum)
				time.sleep(on)
				self.led.setLum(0, 0)
				time.sleep(off)
				if self.quitting:
					return

			time.sleep(2)
			off -= 0.05
			on += 0.001
			#lum += 0.02
		self.quit()

		"""
		maxLum = 0
		while maxLum <= 1:
			i = 0
			while i <= maxLum:
				self.led.setLum(i, i)
				i += 0.01
				time.sleep(0.5)
			self.led.setLum(maxLum, maxLum)
			time.sleep(2)
			time.sleep(2)
			maxLum += 0.1
		"""