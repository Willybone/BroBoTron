import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	""" A class of Bullets fired from the dude """
	def __init__ (self, settings, screen, dude, trajectory, pew):
		# Create a bullet at the dude's location
		super(Bullet, self).__init__()
		self.screen = screen
		if trajectory in ('right', 'left'):
			self.bullet_width = settings.bullet_long
			self.bullet_height = settings.bullet_wide
		else:
			self.bullet_width = settings.bullet_wide
			self.bullet_height = settings.bullet_long		
		
		# Create bullet rect at (0,0) and then set current position
		self.rect = pygame.Rect(0, 0, self.bullet_width, self.bullet_height)
		self.rect.centerx = dude.rect.centerx
		self.rect.centery = dude.rect.centery
		self.color = settings.bullet_color
		if trajectory == 'left':
			self.x_speed_factor = settings.bullet_speed_factor * -1
			self.y_speed_factor = 0
			self.rect.right = dude.rect.left
			self.rect.centery = dude.rect.centery
		elif trajectory == 'up':
			self.x_speed_factor = 0
			self.y_speed_factor = settings.bullet_speed_factor * -1
			self.rect.bottom = dude.rect.top
			self.rect.centerx = dude.rect.centerx
		if trajectory == 'right':
			self.x_speed_factor = settings.bullet_speed_factor
			self.y_speed_factor = 0
			self.rect.left = dude.rect.right
			self.rect.centery = dude.rect.centery
		elif trajectory == 'down':
			self.x_speed_factor = 0
			self.y_speed_factor = settings.bullet_speed_factor		
			self.rect.top = dude.rect.bottom
			self.rect.centerx = dude.rect.centerx

		# Store bullet's position as a decimal
		self.ydec = float(self.rect.y)
		self.xdec = float(self.rect.x)
		
		# Make a sound
		pew.play()
		
	def update(self):
		# Move the bullet upwards
		self.xdec += self.x_speed_factor
		self.ydec += self.y_speed_factor
		# Update the rect position
		self.rect.y = self.ydec
		self.rect.x = self.xdec
		
	def draw_bullet(self):
		# Draw the bullet on the sceen
		pygame.draw.rect(self.screen, self.color, self.rect)
