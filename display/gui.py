import pygame

"""GUI-Handling
	- Event-System fuer ganze GUI
	- Panels mit Activate und deactivate
	- Hierarchien, Container: Display, Screens, Panels
	- Styles (Farben, Fonts, Rahmen)
	- Layout-Raster (Margin, Grid, Float)
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
		self.draw()

	def posInside(self, pos):
		x, y = pos
		return self.rect.collidepoint(x, y)

	def draw(self):
		rect = self.rect.copy()
		rect.topleft = (0,0)
		if self.clicked:
			color = (128,64,0)
		else:
			color = (48,48,48)
		pygame.draw.rect(self.surface, color, rect)
		pygame.draw.rect(self.surface, (16,16,16), rect, 1)
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
		rect.topleft = (0,0)
		pygame.draw.rect(self.surface, (48,48,48), rect)
		pygame.draw.rect(self.surface, (16,16,16), rect, 1)
		rect.inflate_ip(-4, -4)
		rect.width = int(float(rect.width) * self.value)
		pygame.draw.rect(self.surface, (128,64,0), rect)
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