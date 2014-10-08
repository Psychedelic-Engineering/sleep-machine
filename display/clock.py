import pygame, time, math, os, datetime, socket, locale

"""
Simple Digital Clock
- Select Data, format & Size
- Set Font
- Set lightness
"""


class Clock():

	fontname = 'display/fonts/Zapfino.ttf'

	def __init__(self, display):
		self.display = display
		self.surface = self.display.screen
		self.width = self.display.width
		self.height = self.display.height
		self.fontColor = (0,0,0)
		self.timeFont = pygame.font.Font(self.fontname, 64)
		self.dateFont = pygame.font.Font(self.fontname, 19)
		self.addrFont = pygame.font.Font(self.fontname, 12)
		loc = locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
		self.lastTime = ""

	def render(self, force = False):
		timeStr = time.strftime("%H:%M")
		#timeStr = "24:57"
		if timeStr != self.lastTime or force:
			self.surface.fill((0,0,0))
			#self.surface.fill((200,120,70))
			surf = self.timeFont.render(timeStr, True, (255,96,0))
			#self.surface.blit(surf, (2,0))
			size = surf.get_size()
			x = (self.width - size[0]) / 2
			self.surface.blit(surf, (x, -30))

			dateStr = datetime.datetime.now().strftime("%A %d.%B")
			#dateStr = "Donnerstag, 22. September"
			surf = self.dateFont.render(dateStr, True, (255,96,0))
			size = surf.get_size()
			x = (self.width - size[0]) / 2
			self.surface.blit(surf, (x,self.height / 2))
			self.lastTime = timeStr

			"""
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("8.8.8.8",80))
			addrStr = str(s.getsockname()[0])
			s.close()

			surf = self.addrFont.render(addrStr, True, (255,0,0))
			self.screen.blit(surf, (4,220))
			self.surface.blit(surf, (0,200))

			surf = self.addrFont.render("07:30", True, self.fontColor)
			self.surface.blit(surf, (160,220))
			self.surface.blit(surf, (320,540))
			"""
			pygame.display.flip()
