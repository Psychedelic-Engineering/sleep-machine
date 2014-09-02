import pygame


class Display:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		pygame.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.mouse.set_visible(False)

	def __del__(self):
		print "Close PyGame"
		pygame.quit()

	def flip(self):
		pygame.display.flip()

	def misc(self):
		pass
	"""
		#self.surface = pygame.Surface((width, height))
        #self.screen.blit(surf, (320,540))
		#self.surface = pygame.Surface((width, height))

	"""
