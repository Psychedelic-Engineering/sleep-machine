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
		logging.basicConfig(format='%(message)s', level=logging.INFO)
		logging.info("init app")
		self.quitting = False
		self.screenMult = 1

	def initialize(self):
		Peripherals.init()
		if self.emulateSensor:
			self.sensor = FakeSensor()
		else:
			self.sensor = Sensor(Peripherals.devices["Pillow"])
		self.led = LED(Peripherals.devices["Basestation"])
		self.display = Display(self.screenMult*320, self.screenMult*240, self.isRaspberry)
		self.graph = Graph(self.display, self.sensor)
		self.clock = Clock(self.display)
		self.scheduler = Scheduler()
		# ToDo: Alarme in config File, periodisch auslesen
		self.scheduler.addAlarm("*", "22", "00", self.sensor.startLogging)
		self.scheduler.addAlarm("*", "10", "00", self.sensor.stopLogging)
		self.scheduler.addAlarm("*", "15", "46", self.doAlarm)
		self.scheduler.addAlarm("*", "8", "30", self.doAlarm)

	def start(self):
		try:
			logging.info("start app")
			self.initialize()
			logging.info("entering mainloop")
			while True:
				if self.scheduler.elapsed(0.1):
					# ToDo: Sensoren ggf. ueber Scheduler
					self.sensor.readData()
					# toDo: ggf. zentraler Display Manager
					self.clock.render()
					self.graph.render()
					self.scheduler.checkAlarm()
					"""
					for event in pygame.event.get():
						if event.type == pygame.MOUSEBUTTONDOWN:
							pass

					"""


		except:
			self.quit()

	def quit(self):
		logging.info("Quit app")
		Peripherals.close()
		self.quitting = True
		time.sleep(1)
		sys.exit()

	# ToDo: Aktionen auslagern, ggf. eigene klasse. Peripherie etc uebergeben???
	def doAlarm(self):
		import random
		start = time.time()

		warm = 0.0
		cold = 0.0

		while warm <= 0.4:
			self.led.setLum(warm, cold)
			time.sleep(0.1)
			warm += 0.0005

		while cold <= 0.2:
			self.led.setLum(warm, cold)
			time.sleep(0.1)
			cold += 0.0005
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

		t = 10
		for i in range(10):
			self.led.setLum(1, 1)
			time.sleep(10-t)
			self.led.setLum(0, 0)
			time.sleep(t)
			t -= 1

		self.led.setLum(0, 0)
