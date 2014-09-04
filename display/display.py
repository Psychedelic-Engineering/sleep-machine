import os, pygame

"""
	Display Klasse
	- kapselt PyGame
	- notwendig?
	- wer verwaltet High-Level display (Layout, Umschaltung Zeit-Graph etc)
"""


class Display:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		os.environ["SDL_FBDEV"] = "/dev/fb1"
		pygame.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.mouse.set_visible(False)

	def __del__(self):
		pygame.quit()

	def flip(self):
		pygame.display.flip()
