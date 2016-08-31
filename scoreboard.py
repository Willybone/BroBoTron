import pygame.font
from pygame.sprite import Group
from dude import Dude

class Scoreboard():
	""" A class for displaying the score """
	def __init__(self, settings, screen, stats):
		self.settings = settings
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.stats = stats
		
		self.text_color = (50, 50, 50)
		self.font = pygame.font.SysFont(None, 48)
		
		self.prep_score()
		self.prep_high_score()
		self.prep_round()
		self.prep_dudes()
		
	def prep_score(self):
		rounded_score = int(round(self.stats.game_score, -1))		
		score_str = "{:,}".format(rounded_score)		
		self.score_image = self.font.render(score_str, True, 
			self.text_color, self.settings.bg_color)
			
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_high_score(self):
		high_score = int(round(self.stats.high_score, -1))		
		high_score_str = "{:,}".format(high_score)		
		self.high_score_image = self.font.render(high_score_str, True, 
			self.text_color, self.settings.bg_color)
			
		self.high_score_rect = self.score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = 20
		
	def prep_round(self):
		self.round_image = self.font.render(str(self.stats.round_num), True, 
			self.text_color, self.settings.bg_color)
			
		self.round_rect = self.round_image.get_rect()
		self.round_rect.right = self.screen_rect.right - 20
		self.round_rect.top = self.score_rect.bottom + 10
		
	def prep_dudes(self):
		self.dudes = Group()
		for dude_number in range(self.stats.dudes_left):
			dude = Dude(self.settings, self.screen)
			dude.rect.x = 10 + dude_number * dude.rect.width
			dude.rect.y = 10
			self.dudes.add(dude)
		
		
	def show_score(self):
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.round_image, self.round_rect)
		self.dudes.draw(self.screen)
	
