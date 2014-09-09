import pygame, math, time

"""GUI-Handling
	- Event-System fuer ganze GUI
	- Hierarchien & Container: Display, Screens, Panels
	- Styles (Farben, Fonts, Rahmen)
	- Layout-Manager (Margin, Grid, Float)
	- Invalidate Mechanik
"""


class GUI():

	fontname = 'display/fonts/digital-7.ttf'

	def __init__(self, display):
		self.display = display
		self.surface = self.display.screen
		self.width = self.display.width
		self.height = self.display.height
		self.fontColor = (0,0,0)
		self.guiFont = pygame.font.Font(self.fontname, 20)
		self.surface = pygame.Surface((self.width, self.height))
		self.mouseVisible = False
		self.widgets = []
		self.render()

	def addWidget(self, widget):
		self.widgets.append(widget)

	def drawBG(self):
		self.surface.fill((32, 32, 32))

	def handleEvent(self, event):
		for w in self.widgets:
			w.handleEvent(event)

	def render(self):
		if not self.mouseVisible:
			pygame.mouse.set_visible(True)
			self.mouseVisible = True
		self.drawBG()
		for w in self.widgets:
			w.render(self.surface)
		self.display.screen.blit(self.surface, (0, 0))
		pygame.display.flip()


class Widget:

	mouseEvents = (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN)

	def __init__(self, gui, left, top, width, height, name=None, label=None):
		self.gui = gui
		self.label = None
		self.setLabel(label)
		self.name = name
		self.clicked = False
		self.rect = pygame.Rect(left, top, width, height)
		self.setPos(left, top)
		self.setSize(width, height)

	def setLabel(self, text=""):
		self.text = text
		self.label = self.gui.guiFont.render(text, True, (160,160,160))

	def setPos(self, left, top):
		self.rect.left = left
		self.rect.top = top

	def setSize(self, width, height):
		self.rect.width = width
		self.rect.height = height
		self.surface = pygame.Surface((self.rect.width, self.rect.height))
		self.surface.set_colorkey((0,0,0))
		self.draw()

	def posInside(self, pos):
		x, y = pos
		return self.rect.collidepoint(x, y)

	def drawRect(self, rect, fillcolor, lineColor=None):
		#pygame.draw.rect(self.surface, fillcolor, rect)
		RoundRect2(self.surface, fillcolor, rect, 0, 8, 8)
		if lineColor:
			#pygame.draw.rect(self.surface, lineColor, rect, 1)
			RoundRect2(self.surface, lineColor, rect, 1, 8, 8)

	def draw(self):
		rect = self.rect.copy()
		rect.topleft = (0,0)
		if self.clicked:
			color = (128,64,0)
		else:
			color = (48,48,48)
		self.drawRect(rect, color, (16,16,16))
		self.drawLabel()

	def drawLabel(self):
		if self.label is not None:
			lw, lh = self.label.get_size()
			x = (self.rect.width-lw) / 2
			y = (self.rect.height-lh) / 2
			self.surface.blit(self.label, (x,y))

	def render(self, surface):
		self.draw()
		surface.blit(self.surface, self.rect.topleft)

	def handleEvent(self, event):
		event.pos[0] += 10
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.posInside(event.pos):
				self.clicked = True
				self.clickPos = event.pos
				self.draw()
				try:
					self.onClick(self)
				except:
					pass
		if event.type == pygame.MOUSEBUTTONUP:
			if self.clicked:
				self.clicked = False
				self.draw()


class Slider(Widget):
	def __init__(self, gui, left, top, width, height, name=None, label=None):
		self.value = 0.5
		Widget.__init__(self, gui, left, top, width, height, name, label)

	def draw(self):
		rect = self.rect.copy()
		rect.topleft = (0, 0)
		self.drawRect(rect, (48,48,48), (16,16,16))
		rect.inflate_ip(-4, -4)
		rect.width = int(float(rect.width) * self.value)
		self.drawRect(rect, (128,64,0), (64,32,0))
		self.drawLabel()


	def handleEvent(self, event):
		Widget.handleEvent(self, event)
		if self.clicked:
			if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
				x,y = event.pos
				self.value = float(x-self.rect.left) / self.rect.width
				self.value = max(min(self.value, 1.0), 0.0)
				try:
					self.onChange(self, self.value)
				except:
					pass
				self.draw()



def RoundRect2(surface, color, rect, width, xr, yr):
	clip = surface.get_clip()
	surface.set_clip(clip.clip(rect.inflate(0, -yr*2)))
	pygame.draw.rect(surface, color, rect.inflate(1-width,0), width)
	surface.set_clip(clip.clip(rect.inflate(-xr*2, 0)))
	pygame.draw.rect(surface, color, rect.inflate(0,1-width), width)
	surface.set_clip(clip.clip(rect.left, rect.top, xr, yr))
	pygame.draw.ellipse(surface, color, pygame.Rect(rect.left, rect.top, 2*xr, 2*yr), width)
	surface.set_clip(clip.clip(rect.right-xr, rect.top, xr, yr))
	pygame.draw.ellipse(surface, color, pygame.Rect(rect.right-2*xr, rect.top, 2*xr, 2*yr), width)
	surface.set_clip(clip.clip(rect.left, rect.bottom-yr, xr, yr))
	pygame.draw.ellipse(surface, color, pygame.Rect(rect.left, rect.bottom-2*yr, 2*xr, 2*yr), width)
	surface.set_clip(clip.clip(rect.right-xr, rect.bottom-yr, xr, yr))
	pygame.draw.ellipse(surface, color, pygame.Rect(rect.right-2*xr, rect.bottom-2*yr, 2*xr, 2*yr), width)
	surface.set_clip(clip)
