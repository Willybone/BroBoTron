import pygame
from pygame.sprite import Sprite

class Dude(Sprite):
	""" This is the game dude. """
	def __init__(self, settings, screen):
		super(Dude, self).__init__()
		self.screen = screen
		self.settings = settings

		# Get dude image and get its rect.
		self.image = pygame.image.load('images/dude.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		# Start new dude at the bottom center
		self.rect.centerx = self.screen_rect.centerx
		self.rect.centery = self.screen_rect.centery

		# Creating decimal versions of the dude's position for fine control of speed
		self.centerxdec = float(self.rect.centerx)
		self.centerydec = float(self.rect.centery)

		# Setting the action flags
		self.moving_x = 0.0
		self.moving_y = 0.0

	def center_dude(self):
		self.centerxdec = self.screen_rect.right / 2
		self.centerydec = self.screen_rect.bottom / 2

	def blitme(self):
		""" Draw the dude at its current location
		Note that I'm setting the real rect coordinates to the
		rounded float values"""
		self.rect.centerx = self.centerxdec
		self.rect.centery = self.centerydec
		self.screen.blit(self.image, self.rect)

	def update(self):
		""" Change the dude's position. Please note that I'm using
		centerxdec and centerydec, which are floats. These numbers
		are then assigned to rect.centerx and rect.centery prior
		to rendering to the screen """
		self.newcenterxdec = self.centerxdec + (self.moving_x *
				self.settings.dude_speed_factor)
		self.newcenterydec = self.centerydec + (self.moving_y *
				self.settings.dude_speed_factor)
		if self.newcenterxdec > 40 and (self.newcenterxdec <
			self.settings.screen_width - 40):
			self.centerxdec = self.newcenterxdec
		if self.newcenterydec > 40 and (self.newcenterydec <
			self.settings.screen_height -40):
			self.centerydec = self.newcenterydec
