
import time, pygame, sys
from sensors import Sensor
from fakesensor import FakeSensor
from graph import Graph

class SleepApp:

	def __init__(self):
		self.quitting = False
		#self.sensor = Sensor()
		self.sensor = FakeSensor()
		self.graph = Graph(1600, 900, self.sensor)

	def start(self):
		lastTime = 0
		counter = 0
		startTime = 0
		while True:
			now = time.time()
			elapsed = now - lastTime
			if elapsed >= 0.001:
				lastTime = now
				self.sensor.readData()
				#self.graph.render()
				counter += 1
				if (counter % 100) == 0:
					print 100 / (time.time() - startTime)
					startTime = time.time()

	def quit(self):
		print "Quit..."
		self.quitting = True
		pygame.quit()
		time.sleep(1)
		sys.exit()
        
        