import pygame, math

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
		#pygame.draw.rect(self.surface, color, rect)
		#pygame.draw.rect(self.surface, (16,16,16), rect, 1)
		#RoundRect(self.surface, rect, (64,64,64), 0.2)
		#RoundRect2(self.surface,(128,64,64), rect, 0, 10, 10)
		#RoundRect2(self.surface,(255,255,255), rect, 1, 10, 10)
		RoundRect3(self.surface,(255,255,255),(128,64,64),rect,1,20)
		#round_rect(self.surface, rect, (255,255,255), 30, 1, color)
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


def RoundRect(surface, rect, color, radius=0.4):

	rect         = pygame.Rect(rect)
	color        = pygame.Color(*color)
	alpha        = color.a
	color.a      = 0
	pos          = rect.topleft
	rect.topleft = 0,0
	rectangle    = pygame.Surface(rect.size,pygame.SRCALPHA)

	circle       = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA)
	pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
	circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

	radius              = rectangle.blit(circle,(0,0))
	radius.bottomright  = rect.bottomright
	rectangle.blit(circle,radius)
	radius.topright     = rect.topright
	rectangle.blit(circle,radius)
	radius.bottomleft   = rect.bottomleft
	rectangle.blit(circle,radius)

	rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
	rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

	rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
	rectangle.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)

	return surface.blit(rectangle,pos)


def RoundRect2(surface, color, rect, width, xr, yr):
	clip = surface.get_clip()

	# left and right
	surface.set_clip(clip.clip(rect.inflate(0, -yr*2)))
	pygame.draw.rect(surface, color, rect.inflate(1-width,0), width)

	# top and bottom
	surface.set_clip(clip.clip(rect.inflate(-xr*2, 0)))
	pygame.draw.rect(surface, color, rect.inflate(0,1-width), width)

	# top left corner
	surface.set_clip(clip.clip(rect.left, rect.top, xr, yr))
	pygame.draw.ellipse(surface, color, pygame.Rect(rect.left, rect.top, 2*xr, 2*yr), width)

	# top right corner
	surface.set_clip(clip.clip(rect.right-xr, rect.top, xr, yr))
	pygame.draw.ellipse(surface, color, pygame.Rect(rect.right-2*xr, rect.top, 2*xr, 2*yr), width)

	# bottom left
	surface.set_clip(clip.clip(rect.left, rect.bottom-yr, xr, yr))
	pygame.draw.ellipse(surface, color, pygame.Rect(rect.left, rect.bottom-2*yr, 2*xr, 2*yr), width)

	# bottom right
	surface.set_clip(clip.clip(rect.right-xr, rect.bottom-yr, xr, yr))
	pygame.draw.ellipse(surface, color, pygame.Rect(rect.right-2*xr, rect.bottom-2*yr, 2*xr, 2*yr), width)

	surface.set_clip(clip)

def RoundRect3(surface,BorderColor,FillColor,(posx,posy,dimensionx,dimensiony),width,roundedness):
	for x in xrange(roundedness,0-1,-1):
		y = math.sqrt((roundedness**2)-(x**2))
		rect = (posx+(roundedness-x),
		        posy+(roundedness-y),
		        dimensionx-(2*(roundedness-x)),
		        dimensiony-(2*(roundedness-y)))
		pygame.draw.rect(surface,BorderColor,rect,0)
	for x in xrange(roundedness-width,0-1,-1):
		y = math.sqrt(((roundedness-width)**2)-(x**2))
		rect = (posx+(roundedness-x),
		        posy+(roundedness-y),
		        dimensionx-(2*(roundedness-x)),
		        dimensiony-(2*(roundedness-y)))
		pygame.draw.rect(surface,FillColor,rect,0)


from pygame import gfxdraw


def round_rect(surface, rect, color, rad=20, border=0, inside=(0,0,0,0)):
	"""
	Draw a rect with rounded corners to surface.  Argument rad can be specified
	to adjust curvature of edges (given in pixels).  An optional border
	width can also be supplied; if not provided the rect will be filled.
	Both the color and optional interior color (the inside argument) support
	alpha.
	"""
	rect = pygame.Rect(rect)
	zeroed_rect = rect.copy()
	zeroed_rect.topleft = 0,0
	image = pygame.Surface(rect.size).convert_alpha()
	image.fill((0,0,0,0))
	_render_region(image, zeroed_rect, color, rad)
	if border:
		zeroed_rect.inflate_ip(-2*border, -2*border)
		_render_region(image, zeroed_rect, inside, rad)
	surface.blit(image, rect)


def _render_region(image, rect, color, rad):
	"""Helper function for round_rect."""
	corners = rect.inflate(-2*rad, -2*rad)
	for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
		pygame.draw.circle(image, color, getattr(corners,attribute), rad)
	image.fill(color, rect.inflate(-2*rad,0))
	image.fill(color, rect.inflate(0,-2*rad))


def aa_round_rect(surface, rect, color, rad=20, border=0, inside=(0,0,0)):
	"""
	Draw an antialiased rounded rect on the target surface.  Alpha is not
	supported in this implementation but other than that usage is identical to
	round_rect.
	"""
	rect = pygame.Rect(rect)
	_aa_render_region(surface, rect, color, rad)
	if border:
		rect.inflate_ip(-2*border, -2*border)
		_aa_render_region(surface, rect, inside, rad)


def _aa_render_region(image, rect, color, rad):
	"""Helper function for aa_round_rect."""
	corners = rect.inflate(-2*rad-1, -2*rad-1)
	for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
		x, y = getattr(corners, attribute)
		gfxdraw.aacircle(image, x, y, rad, color)
		gfxdraw.filled_circle(image, x, y, rad, color)
	image.fill(color, rect.inflate(-2*rad,0))
	image.fill(color, rect.inflate(0,-2*rad))