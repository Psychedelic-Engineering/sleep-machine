import time, datetime
import sys
from display.display import Display
from fakesensor import FakeSensor
from sensors import Sensor
from display.graph import Graph
from display.clock import Clock
from teensy import Peripherals
from scheduler import Scheduler


class SleepApp:

	def __init__(self):
		self.quitting = False
		Peripherals.init()
		#self.sensor = Sensor(Peripherals.devices["Pillow"])
		#self.sensor = FakeSensor()
		self.display = Display(320, 240)
		#self.graph = Graph(self.display, self.sensor)
		self.clock = Clock(self.display)
		self.scheduler = Scheduler()

		#self.sensor.startLogging()

	def start(self):
		while True:
			if self.scheduler.elapsed(0.02):
				#self.sensor.readData()
				self.clock.render()
				#self.graph.render((1,2,3))
				#self.scheduler.check()

	def quit(self):
		print "Quit..."
		self.quitting = True
		time.sleep(1)
		sys.exit()
