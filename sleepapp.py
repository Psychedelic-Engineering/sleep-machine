import time
import logging
import sys
import os
import pygame

from hardware.teensy import Peripherals
from hardware.fakesensor import FakeSensor
from hardware.sensors import Sensor
from display.display import Display
from display.graph import Graph
from display.clock import Clock
from display.settings import Settings
from events.scheduler import Scheduler
import actions


class SleepApp:

	def __init__(self):
		self.isRaspberry = False
		self.emulateSensor = True
		logging.basicConfig(format='%(message)s', level=logging.INFO)
		logging.info("init app")
		self.quitting = False

	def __del__(self):
		self.quit()

	def initialize(self):
		Peripherals.init()
		if self.emulateSensor:
			self.sensor = FakeSensor()
		else:
			self.sensor = Sensor(Peripherals.devices["Pillow"])
		#self.led = LED(Peripherals.devices["Basestation"])
		#self.led.setLum(0, 0)

		# toDo: ggf. zentraler Display Manager
		self.screenMult = 4
		#self.display = Display(self.screenMult*320, self.screenMult*240, self.isRaspberry)
		self.display = Display(1024, 600, self.isRaspberry)
		#self.graph = Graph(self.display, self.sensor)
		self.clock = Clock(self.display)
		self.settings = Settings(self.display)
		self.settings.onButton = self.onButton
		self.settings.onSetLight = self.onSetLight

		self.scheduler = Scheduler()
		# ToDo: Alarme in config File, periodisch auslesen
		self.scheduler.addAlarm("*", "7", "00", actions.switchRelais)
		#self.scheduler.addAlarm("*", "*", "2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58", actions.switchRelais)
		self.scheduler.addAlarm("*", "21", "21", actions.switchRelais)

	def onButton(self, action):
		if action == "close":
			self.guiMode = False
			self.clock.render(force=True)
		elif action == "quit":
			self.quit()
		elif action == "reboot":
			os.system("/sbin/reboot")

	def onSetLight(self, warm, cold):
		self.led.setLum(warm, cold)

	def start(self):
		try:
			logging.info("start app")
			self.initialize()
			logging.info("entering mainloop")
			self.guiMode = False
			while True:
				if self.quitting:
					break
				if self.scheduler.elapsed(0.05):
					# ToDo: Sensoren ggf. ueber Scheduler
					self.sensor.readData()
					self.scheduler.checkAlarm()
					# toDo: ggf. zentraler Display Manager
					if self.guiMode:
						self.settings.render()
					else:
						self.clock.render()
						#self.graph.render()
					# ToDo: Eventhandling in GUI
					for event in pygame.event.get():
						if not self.guiMode:
							if event.type == pygame.MOUSEBUTTONDOWN:
								self.guiMode = True
						else:
							self.settings.handleEvent(event)
		except Exception as e:
			raise
		finally:
			pass
			#self.quit()

	def quit(self):
		#ToDo: Saubere Deinitialisierung und Threadsynchronisation
		self.quitting = True
		logging.info("Quit app")
		Peripherals.close()
		time.sleep(1)
		sys.exit()
