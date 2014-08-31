import pygame
import numpy as np


class Graph:
	def __init__(self, width, height, sensor):
		self.sensor = sensor
		self.width = width
		self.height = height
		pygame.init()
		pygame.font.init()
		self.surface = pygame.display.set_mode((self.width, self.height))
		#self.surface = pygame.Surface((width, height))
		self.drawBG()

		self.curX = 0
		self.x = 0
		self.colors = (
		(128, 128, 128),
		(255, 0, 0),
		(255, 255, 0),
		(0, 255, 255),
		(255, 255, 255),
		(255, 255, 255),
		(255, 255, 255),
		(128, 255, 255),
		(255, 128, 255),
		(255, 255, 128),
		(255, 255, 255),
		(255, 255, 255),
		(0, 128, 128)
		)

		#self.sensor.channels[0].onUpdate = self.updateBuffer

	bufferX = 0

	def updateBuffer(self, channel):
		min = 1000
		max = 2000
		buffer = channel.npBuffer

		if self.bufferX >= (self.width - 1):
			self.bufferX = 0
			self.drawBG()
		for i in np.nditer(buffer):
			y = int(self.map_value(i, min, max, self.height, 0))
			self.surface.set_at((self.bufferX, y), self.colors[0])
			self.bufferX += 1
			print self.bufferX, i

		pygame.display.flip()



	def drawBG(self):
		self.surface.fill((0, 0, 0))
		for i in range(10):
			y = int(self.map_value(i * 50, -100, 600, self.height, 0))
			pygame.draw.line(self.surface, (64,64,64), (0,y), (self.width,y))

	def draw(self, channel):
		pass

	def setValues(self, values):
		self.values = values

	def render(self, channels=None):
		#return
		if self.x >= (self.width - 1):
			self.x = 0
			self.drawBG()

		#self.surface.scroll(-1,0)
		#pygame.draw.rect(self.surface, (0,0,0), (self.width-1, 0, 2, self.height))
		#x = self.width-1
		else:
			self.x += 1
		#for i, value in enumerate(self.values):
		#	if channels is None or i in channels:

		#for i, channel in enumerate(self.sensor.channels):
		channel = self.sensor.channels[1]
		self.renderChannel(channel, self.colors[1])

		pygame.display.flip()

	#self.screen.blit(self.surface, (0,0))

	def renderChannel(self, channel, color):
		min = channel.min
		max = channel.max + 500

		value = channel.getValue()
		y = int(self.map_value(value, min, max, self.height, 0))

		avg = channel.getBufferAvg()
		yAvg = int(self.map_value(avg, min, max, self.height, 0))

		rng = channel.getRng()
		yRng = int(self.map_value(rng, 0, 1000, self.height, 0))

		#self.surface.set_at((self.x, yRng), self.colors[2])
		self.surface.set_at((self.x, y), self.colors[1])
		self.surface.set_at((self.x, yAvg), self.colors[2])




	def map_value(self, value, in_min, in_max, out_min, out_max):
		return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min