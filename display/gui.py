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
		self.slider = (20,100,280,100)
		self.close = (280,0,40,40)
		self.lum = 0
		self.drawBG()

	def drawBG(self):
		self.surface.fill((64, 64, 64))

	def handleEvent(self, event):
		if event.type == pygame.MOUSEMOTION:
			x,y = event.pos
			if self.insideRect(event.pos, self.slider):
				self.lum = self.sliderPos(x, self.slider)
				self.drawSlider()
				self.onSetLight(self.lum)

		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.insideRect(event.pos, self.close):
				self.drawBG()
				self.onClose()



	def render(self):
		self.drawBG()
		self.drawClose()
		self.drawSlider()
		self.display.screen.blit(self.surface, (0, 0))
		pygame.display.flip()


	def drawClose(self):
		pygame.draw.rect(self.surface, (255,0,0), self.close, 2)

	def drawSlider(self):
		l, t, w, h = self.slider
		pygame.draw.rect(self.surface, (255,0,0), self.slider, 2)
		w = int(float(w) * self.lum)
		pygame.draw.rect(self.surface, (255,255,0), [l, t, w, h])



	def insideRect(self, pos, rect):
		x, y = pos
		l,t,w,h = rect
		return l < x < (l+w) and t < y < (t+h)

	def sliderPos(self, x, rect):
		l,t,w,h = rect
		return float(x - l) / w