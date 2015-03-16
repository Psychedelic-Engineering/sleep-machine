import os, pygame, logging

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
		os.environ["SDL_MOUSEDEV"] = "/dev/input/event1"
		os.environ["SDL_MOUSEDRV"] = "TSLIB"

		pygame.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode((self.width, self.height))
		#pygame.mouse.set_visible(False)
		logging.info(pygame.display.get_driver())
		logging.info(pygame.display.get_wm_info())
		logging.info(pygame.display.Info())

	def __del__(self):
		logging.debug("pygame.quit")
		pygame.quit()

	def flip(self):
		pygame.display.flip()
