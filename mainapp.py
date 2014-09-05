import time, logging, sys
from display.display import Display
from fakesensor import FakeSensor
from sensors import Sensor
from display.graph import Graph
from display.clock import Clock
from teensy import Peripherals
from scheduler import Scheduler


class SleepApp:

	def __init__(self):
		logging.basicConfig(format='%(message)s', level=logging.DEBUG)
		logging.debug("init app")
		self.quitting = False
		Peripherals.init()
		self.sensor = Sensor(Peripherals.devices["Pillow"])
		#self.sensor = FakeSensor()
		self.led = Peripherals.devices["Basestation"]
		self.display = Display(320, 240)
		self.graph = Graph(self.display, self.sensor)
		self.clock = Clock(self.display)
		self.scheduler = Scheduler()
		#self.sensor.startLogging()

		self.scheduler.addAlarm("*", "*", "10,20,30,40,50,0", self.doAlarm)

	def start(self):
		logging.debug("start app")
		while True:
			if self.scheduler.elapsed(0.2):
				self.sensor.readData()
				self.clock.render()
				self.graph.render()
				self.scheduler.checkAlarm()

	def quit(self):
		logging.debug("Quit app")
		Peripherals.close()
		self.quitting = True
		time.sleep(1)
		sys.exit()

	def doAlarm(self):
		steps = 1000
		for i in range(steps):
			lum = float(i) / steps
			cmd = "w %f c %f\n" % (lum, lum / 2)
			self.led.sendCommand(cmd)
		#time.sleep(1)
		self.led.sendCommand("c 0 w 0\n")