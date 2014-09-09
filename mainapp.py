import time, logging, sys, os
from display.display import Display
from fakesensor import FakeSensor
from sensors import Sensor
from display.graph import Graph
from display.clock import Clock
from display.settings import Settings
from teensy import Peripherals
from scheduler import Scheduler
import pygame
from basestation import LED


class SleepApp:

	def __init__(self):
		pygame.mixer.pre_init(44100, -16, 2, 4096)
		self.isRaspberry = True
		self.emulateSensor = True
		logging.basicConfig(format='%(message)s', level=logging.INFO)
		logging.info("init app")
		self.quitting = False
		self.screenMult = 1

	def __del__(self):
		self.quit()

	def initialize(self):
		Peripherals.init()
		if self.emulateSensor:
			self.sensor = FakeSensor()
		else:
			self.sensor = Sensor(Peripherals.devices["Pillow"])
		#self.led = LED(Peripherals.devices["Basestation"])
		self.display = Display(self.screenMult*320, self.screenMult*240, self.isRaspberry)
		# toDo: ggf. zentraler Display Manager
		self.graph = Graph(self.display, self.sensor)
		self.clock = Clock(self.display)
		self.settings = Settings(self.display)
		self.settings.onButton = self.onButton
		self.settings.onSetLight = self.onSetLight

		self.scheduler = Scheduler()
		# ToDo: Alarme in config File, periodisch auslesen
		self.scheduler.addAlarm("*", "22", "00", self.sensor.startLogging)
		self.scheduler.addAlarm("*", "10", "00", self.sensor.stopLogging)
		self.scheduler.addAlarm("*", "21", "00", self.doAlarm)
		self.scheduler.addAlarm("*", "7", "30", self.doAlarm)

	def onButton(self, action):
		if action == "close":
			self.guiMode = False
			self.clock.render(force=True)
		elif action == "quit":
			self.quit()
		elif action == "reboot":
			pygame.mixer.init()
			pygame.mixer.music.load('Anhalter.mp3')
			pygame.mixer.music.play()
			#os.system("/sbin/reboot")

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
				if self.scheduler.elapsed(0.1):
					# ToDo: Sensoren ggf. ueber Scheduler
					self.sensor.readData()
					self.scheduler.checkAlarm()
					# toDo: ggf. zentraler Display Manager
					if self.guiMode:
						self.settings.render()
					else:
						self.clock.render()
						self.graph.render()
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

	# ToDo: Aktionen auslagern, ggf. eigene klasse. Peripherie etc uebergeben???
	def doAlarm(self):
		import random
		for i in range(5):
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
