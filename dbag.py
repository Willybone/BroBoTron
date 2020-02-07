import pygame
from pygame.sprite import Sprite
from random import randint


class Dbag(Sprite):
	def __init__(self, screen, settings):
		super(Dbag, self).__init__()
		self.screen = screen
		self.settings = settings

		dbag_selector = randint(1,4)
		if dbag_selector == 1:
			self.image = pygame.image.load('images/squirt.bmp')
		elif dbag_selector == 2:
			self.image = pygame.image.load('images/beedrill.bmp')
		elif dbag_selector == 3:
			self.image = pygame.image.load('images/bulbasaur.bmp')
		elif dbag_selector == 4:
			self.image = pygame.image.load('images/koffing.bmp')

		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		self.side_select = randint(1,4)
		if self.side_select == 1:
			self.rect.centerx = randint(self.screen_rect.left + 5, self.screen_rect.right - 5)
			self.rect.bottom = 0
		if self.side_select == 2:
			self.rect.left = self.screen_rect.right
			self.rect.centery = randint(self.screen_rect.top + 5, self.screen_rect.bottom - 5)
		if self.side_select == 3:
			self.rect.centerx = randint(self.screen_rect.left + 5, self.screen_rect.right - 5)
			self.rect.top = self.screen_rect.bottom
		if self.side_select == 4:
			self.rect.right = 0
			self.rect.centery = randint(self.screen_rect.top + 5, self.screen_rect.bottom - 5)

		self.xdec = float(self.rect.x)
		self.ydec = float(self.rect.y)

		self.xmove = 0
		self.ymove = 0
		self.step_count = 0

	def update(self, settings, screen, stats, dude):
		if self.step_count >= settings.dbag_max_steps:
			self.update_direction(dude)
		else:
			self.step_count += 1
		self.xdec += (self.xmove * (settings.dbag_speed_factor +
			(stats.round_num * settings.round_speed_increase)))
		self.ydec += (self.ymove * (settings.dbag_speed_factor +
			(stats.round_num * settings.round_speed_increase)))
		self.rect.x = self.xdec
		self.rect.y = self.ydec

	def blitme(self):
		self.screen.blit(self.image, self.rect)
		
	def update_direction(self, dude):
		if dude.rect.centerx > self.rect.centerx:
			self.xmove = 1
		else:
			self.xmove = -1

		if dude.rect.centery > self.rect.centery:
			self.ymove = 1
		else:
			self.ymove = -1

		self.step_count=0
