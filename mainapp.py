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
		self.isRaspberry = True
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
		self.scheduler.addAlarm("*", "22", "00", self.sensor.startLogging)
		self.scheduler.addAlarm("*", "10", "00", self.sensor.stopLogging)
		self.scheduler.addAlarm("*", "20", "00", self.doAlarm)
		self.scheduler.addAlarm("*", "8", "30", self.doAlarm)
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
		import random
		start = time.time()

		warm = 0.0
		cold = 0.0

		while warm <= 0.4:
			self.led.setLum(warm, cold)
			time.sleep(0.1)
			warm += 0.0005
		print time.time() - start

		while cold <= 0.2:
			self.led.setLum(warm, cold)
			time.sleep(0.1)
			cold += 0.0005
		print time.time() - start

		print "Gewitter"
		cnt = 0.01
		len = 0.01

		while time.time() < start+300:
			if random.random() < cnt:
				self.led.setLum(1, 1)
				time.sleep(len)
				if len <= 0.1:
					len += 0.0005
			self.led.setLum(warm, cold)
			time.sleep(0.1)
			if cnt <= 0.2:
				cnt += 0.0002
		print time.time() - start

		t = 10
		for i in range(10):
			self.led.setLum(1, 1)
			time.sleep(10-t)
			self.led.setLum(0, 0)
			time.sleep(t)
			t -= 1
		print time.time() - start

		self.led.setLum(0, 0)
