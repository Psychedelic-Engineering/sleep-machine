import time
import sys
from display.display import Display
from fakesensor import FakeSensor
from sensors import Sensor
from display.graph import Graph
from display.clock import Clock


class SleepApp:

	def __init__(self):
		self.quitting = False
		self.sensor = Sensor()
		#self.sensor = FakeSensor()
		self.display = Display(320, 240)
		self.graph = Graph(self.display, self.sensor)
		self.clock = Clock(self.display)

	def start(self):
		lastTime = 0
		counter = 0
		startTime = 0
		while True:
			now = time.time()
			elapsed = now - lastTime
			if elapsed >= 0.0005:
				lastTime = now
				self.sensor.readData()
				self.clock.render()
				self.graph.render((1,2,3))
				counter += 1
				if (counter % 100) == 0:
					print 100 / (time.time() - startTime)
					startTime = time.time()

	def quit(self):
		print "Quit..."
		self.quitting = True
		time.sleep(1)
		sys.exit()
