import pygame, time, math, os, datetime, socket, locale

class GUI():

	fontname = 'display/fonts/digital-7.ttf'

	def __init__(self, display):
		self.display = display
		self.surface = self.display.screen
		self.width = self.display.width
		self.height = self.display.height
		self.fontColor = (0,0,0)
		self.guiFont = pygame.font.Font(self.fontname, 14)
		self.surface = pygame.Surface((self.width, self.height))
		self.slider1 = (20,50,280,50)
		self.slider2 = (20,150,280,50)
		self.close = (280,0,40,40)
		self.lumWarm = 0
		self.lumCold = 0
		self.drawBG()

	def drawBG(self):
		self.surface.fill((64, 64, 64))

	def handleEvent(self, event):
		if event.type == pygame.MOUSEMOTION:
			x,y = event.pos
			if self.insideRect(event.pos, self.slider1):
				self.lumWarm = self.sliderPos(x, self.slider1)
				self.render()
				self.onSetLight(self.lumWarm, self.lumCold)

			if self.insideRect(event.pos, self.slider2):
				self.lumCold = self.sliderPos(x, self.slider2)
				self.render()
				self.onSetLight(self.lumWarm, self.lumCold)

		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.insideRect(event.pos, self.close):
				self.onClose()

	def render(self):
		self.drawBG()
		self.drawClose()
		self.drawSlider(self.slider1, self.lumWarm)
		self.drawSlider(self.slider2, self.lumCold)
		self.display.screen.blit(self.surface, (0, 0))
		pygame.display.flip()

	def drawClose(self):
		pygame.draw.rect(self.surface, (255,0,0), self.close, 2)

	def drawSlider(self, slider, value):
		l, t, w, h = slider
		pygame.draw.rect(self.surface, (255,0,0), slider, 2)
		w = int(float(w) * value)
		pygame.draw.rect(self.surface, (255,255,0), [l, t, w, h])

	def insideRect(self, pos, rect):
		x, y = pos
		l,t,w,h = rect
		return l < x < (l+w) and t < y < (t+h)

	def sliderPos(self, x, rect):
		l,t,w,h = rect
		return float(x - l) / w
