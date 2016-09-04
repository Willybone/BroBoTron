# Importing sys, pygame, and game settings class

import sys
import pygame
from pygame.sprite import Group
from pygame.sprite import Sprite
from settings import Settings
from dude import Dude
from bullet import Bullet
from dbag import Dbag
from button import Button
from scoreboard import Scoreboard
import game_functions as gf
from gamestats import GameStats


def run_game():
	# Initialize game. Create a screen
	pygame.init()
	settings = Settings()
	screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
	pygame.display.set_caption("BroBo-Tron")
	
	# Initialize the joysticks
	pygame.joystick.init()
	joystick = pygame.joystick.Joystick(0)
	joystick.init()
	# Make a dude
	dude = Dude(settings, screen)
	# Make a Group for bullets
	bullets = Group()
	bullet_rate = settings.bullet_rate
	bullet_count = settings.bullet_rate
	# Make a Group of dbags
	dbags = Group()
	# Start games stats
	stats = GameStats(settings)
	scoreboard = Scoreboard(settings, screen, stats)
	# Play button
	play_button = Button(settings, screen, "Play")
	
	# Start the main loop for the game
	while True:
		# Listen for events and quit command
		gf.check_events(settings, screen, stats, dbags, dude, bullets, play_button, scoreboard)
		gf.check_joystick(settings, screen, joystick, dude, bullets, bullet_count)
		if bullet_count < bullet_rate:
			bullet_count += 1
		else:
			bullet_count = 0
		
		if stats.game_active:
			# Update the dude, bullets, screen
			dude.update()
			gf.update_dbags(dbags, screen, settings, stats, dude, bullets, scoreboard)
			gf.update_bullets(bullets, settings, dbags, stats, scoreboard)
			
		gf.update_screen(settings, screen, stats, dude, bullets, dbags, play_button, scoreboard)

run_game()
