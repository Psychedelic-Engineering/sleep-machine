import pygame, math
import numpy as np


class Graph():

	def __init__(self, display, sensor):
		self.heightPercent = 1.0 / 3
		self.display = display
		self.sensor = sensor
		self.width = self.display.width
		self.height = self.display.height * self.heightPercent
		self.x = 0
		self.colors = (
		(128, 0, 0),		(0, 128, 0),	(0, 0, 128),
		(96, 96, 0),		(0, 96, 96),	(96, 0, 96),
		(128, 96, 0),		(96, 128, 0),	(0, 96, 128),
		(0, 128, 96))

		self.surface = pygame.Surface((self.width, self.height))
		self.drawBG()
		#self.sensor.channels[1].onUpdate = self.updateBuffer

	def render(self, channels=None):
		self.checkBounds()
		for i, channel in enumerate(self.sensor.channels):
			if channels is None or i in channels:
				self.renderChannel(channel, self.colors[i])

		if self.x % 10 == 0:
			self.display.screen.blit(self.surface, (0, self.display.height - self.height))
			#self.display.screen.blit(self.surface, (0, 0))
			pygame.display.flip()

	def renderChannel(self, channel, color):
		# ggf. funktion, min, max und offset als parameter
		#value = channel.getValue()
		value = channel.getBufferAvg()
		#value = channel.getRng()
		#value = channel.getDiff()
		#value = math.pow(20 * value, 4)
		y = int(self.map_value(value, channel.min, channel.max, self.height, 0))
		self.surface.set_at((self.x, y), color)

	def checkBounds(self, scroll=False):
		if self.x >= (self.width - 1):
			if scroll:
				self.surface.scroll(-1, 0)
				pygame.draw.rect(self.surface, (0, 0, 0), (self.width - 1, 0, 2, self.height))
				self.x -= 1
			else:
				self.x = 0
				self.drawBG()
		else:
			self.x += 1

	def drawBG(self):
		self.surface.fill((0, 0, 0))
		for i in range(10):
			y = int(self.map_value(i, 0, 10, self.height, 0))
			pygame.draw.line(self.surface, (32, 32, 32), (0, y), (self.width, y))

	def map_value(self, value, in_min, in_max, out_min, out_max):
		return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

	"""
	def updateBuffer(self, channel):

		min = 1200
		max = 2000
		buffer = channel.npBuffer
		buffer = channel.smoothed
		std = np.std(channel.npBuffer) + 1200
		var = np.var(channel.npBuffer) * 0.1 + 1200
		avg = np.average(channel.npBuffer)
		mean = np.mean(channel.npBuffer)
		quant = 50
		val = int(avg / quant) * quant

		#for i in np.nditer(buffer):
		for i in range(buffer.shape[0]):
			self.checkBounds()
			value = buffer[i]
			y = int(self.map_value(value, min, max, self.height, 0))
			self.surface.set_at((self.x, y), self.colors[1])

			#smooth = smoothed[i]
			#y = int(self.map_value(smooth, min, max, self.height, 0))
			#self.surface.set_at((self.x, y), self.colors[1])

			y = int(self.map_value(var, min, max, self.height, 0))
			self.surface.set_at((self.x, y), self.colors[2])
			y = int(self.map_value(std, min, max, self.height, 0))
			self.surface.set_at((self.x, y), self.colors[3])
			y = int(self.map_value(val, min, max, self.height, 0))
			#self.surface.set_at((self.x, y), self.colors[4])

			self.x += 1
		pygame.display.flip()

	def draw(self, channel):
		pass

	def setValues(self, values):
		self.values = values

	def render(self, channels=None):
		self.checkBounds()

		self.renderChannel(self.sensor.channels[0], self.colors[1])
		self.renderChannel(self.sensor.channels[1], self.colors[2])
		self.renderChannel(self.sensor.channels[2], self.colors[3])

		pygame.display.flip()
		#self.surface.blit(self.surface, (0,0))



	"""