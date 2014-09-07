import os, pygame

"""Display Klasse
	- notwendig?
	- wer verwaltet High-Level display (Layout, Umschaltung Zeit-Graph etc)
"""


class Display:
	def __init__(self, width, height, isRaspberry=False):
		self.width = width
		self.height = height
		self.isRaspberry = isRaspberry
		if self.isRaspberry:
			os.environ["SDL_FBDEV"] = "/dev/fb1"
			os.environ['SDL_VIDEODRIVER'] = 'fbcon'
			os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
			os.environ["SDL_MOUSEDRV"] = "TSLIB"

		pygame.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode((self.width, self.height))
		#pygame.mouse.set_visible(False)

	def __del__(self):
		pygame.quit()

	def flip(self):
		pygame.display.flip()
