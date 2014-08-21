import pygame


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

	def drawBG(self):
		self.surface.fill((0, 0, 0))
		for i in range(10):
			y = int(self.map_value(i * 50, -100, 600, self.height, 0))
			pygame.draw.line(self.surface, (64,64,64), (0,y), (self.width,y))

	def setValues(self, values):
		self.values = values

	def render(self, channels=None):
		pass

		if self.x >= (self.width - 1):
			self.x = 0
			self.drawBG()

		#self.surface.scroll(-1,0)
		#pygame.draw.rect(self.surface, (0,0,0), (self.width-1, 0, 2, self.height))
		#x = self.width-1
		else:
			self.x += 1
		for i, value in enumerate(self.values):
			if channels is None or i in channels:
				col = self.colors[i]
				min = self.sensor.channels[i].min
				max = self.sensor.channels[i].max
				y = int(self.map_value(value, min, max, self.height, 0))
				self.surface.set_at((self.x, y), col)

		pygame.display.flip()

	#self.screen.blit(self.surface, (0,0))


	def map_value(self, value, in_min, in_max, out_min, out_max):
		return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min