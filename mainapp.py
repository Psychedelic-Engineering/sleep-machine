
import time, pygame, sys
from sensors import Sensor
from fakesensor import FakeSensor
from graph import Graph


class SleepApp:

	def __init__(self):
		self.quitting = False
		self.sensor = FakeSensor()
		self.graph = Graph(1600, 900, self.sensor)

	def start(self):

		lastTime = 0

		while True:
			now = time.time()
			elapsed = now - lastTime
			if elapsed >= 0.0001:
				self.sensor.readData()
				#values = self.sensor.getAvgs()
				#values = self.sensor.getValues()
				#self.graph.setValues(values)
				#v1 = self.sensor.getValues()[0]
				#v2 = self.sensor.getDerivs()[0]
				#v3 = self.sensor.getAvgs()[0]
				#self.graph.setValues((v1, v2, v3))
				#self.graph.render((1, 2, 3))
				self.graph.render()
				#self.graph.render()

				lastTime = time.time()


	def quit(self):
		print "Quit..."
		self.quitting = True
		pygame.quit()
		time.sleep(1)
		sys.exit()
        
        