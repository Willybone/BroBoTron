import sys
import pygame
import math
from pygame.sprite import Group
from bullet import Bullet
from dbag import Dbag
from time import sleep

def check_events():
	# Checking for events coming in
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event)


def check_keydown_events(event):
	# Check keys being pressed and assign actions
	if event.key == 27:
		sys.exit()
		
		

def check_joystick(settings, screen, stats, joystick, dude, dbags, scoreboard, bullets, bullet_count, pew):
	if joystick.get_button(7): 
		if not stats.game_active:
			if stats.game_over:
				start_game(settings, stats, dbags, bullets, dude, scoreboard)
			else:
				stats.game_active = True
		else:
			stats.game_active = False
		
	# Movement measurement and assignment
	x1_axis = joystick.get_axis(0)
	y1_axis = joystick.get_axis(1)
	if abs(x1_axis) > .1:
		dude.moving_x = x1_axis
	else:
		dude.moving_x = 0
	if abs(y1_axis) > .1:
		dude.moving_y = y1_axis
	else:
		dude.moving_y = 0
	
	# Shooting measurement and bullet creation
	x2_axis = joystick.get_axis(4)
	y2_axis = (joystick.get_axis(3) * -1)
	if (abs(x2_axis) > 0.2) or (abs(y2_axis) > 0.2):
		angle = math.atan2(y2_axis, x2_axis)
		if abs(angle) <= (math.pi/4):
			trajectory='right'
		elif angle > (math.pi/4) and angle <= (math.pi*3/4):
			trajectory='up'
		elif abs(angle) > (math.pi*3/4):
			trajectory='left'
		elif angle < (math.pi/-4) and angle >= (math.pi*-3/4):
			trajectory='down'
		
		# Check if it's time to spit out a bullet
		if (bullet_count >= settings.bullet_rate) and (len(bullets) 
			< settings.bullet_max_num):
			new_bullet = Bullet(settings, screen, dude, trajectory, pew)
			bullets.add(new_bullet)
			pew.play()


def update_screen(settings, screen, stats, dude, bullets, dbags, play_button, scoreboard):
	""" Update the screen and flip to the new screen """
	# Refresh the background and redraw the dude and bullets
	screen.fill(settings.bg_color)
	for dbag in dbags:
		dbag.blitme()
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	dude.blitme()
	scoreboard.show_score()
	
	# Draw play button if the game isn't active
	if not stats.game_active:
		play_button.draw_button()
	
	# Make the recently drawn screen visible
	pygame.display.flip()


def update_bullets(bullets, settings, dbags, stats, scoreboard):
	""" Updating bullet position and cleaning up off-screen bullets """
	# Position
	bullets.update()
	# Detect bullet dbag collisions and remove both
	collisions = pygame.sprite.groupcollide(bullets, dbags, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.game_score += len(aliens) * settings.dbag_points
			stats.round_dbags_killed += len(aliens)
			scoreboard.prep_score()
		check_high_score(stats, scoreboard)
		
	# Bullet clean-up
	for bullet in bullets.copy():
		if (bullet.rect.bottom <= 0) or (bullet.rect.right <= 0) or (
			bullet.rect.left >= settings.screen_width) or (
			bullet.rect.top >= settings.screen_height):
			bullets.remove(bullet)


def update_dbags(dbags, screen, settings, stats, dude, bullets, 
	scoreboard):
	create_dbags(dbags, screen, settings, stats)
	dbags.update(settings, screen, stats, dude)
	# Check for end of round
	if stats.round_dbags_killed >= (10 + (5 * stats.round_num)):
		win_round(settings, dbags, stats, dude, bullets, scoreboard)
	# Detect collisions
	if pygame.sprite.spritecollideany(dude, dbags):
		lose_round(dbags, screen, settings, stats, scoreboard, dude, bullets)
	
	
def create_dbags(dbags, screen, settings, stats):
	if (len(dbags) < settings.dbag_starting_num + (stats.round_num * 
		settings.round_dbag_wave_increase)) and (
		(stats.round_dbags_killed + len(dbags)) < (10 + (5 * stats.round_num))):
		dbag = Dbag(screen, settings)
		dbags.add(dbag)
		
		
def check_high_score(stats, scoreboard):
	if stats.game_score > stats.high_score:
		stats.high_score = stats.game_score
		scoreboard.prep_high_score()
		
		
def start_game(settings, stats, dbags, bullets, dude, scoreboard):
		pygame.mouse.set_visible = False
		stats.reset_stats()
		scoreboard.prep_score()
		scoreboard.prep_round()
		scoreboard.prep_dudes()
		settings.initialize_dynamic_settings()
		stats.game_active = True
		stats.game_over = False
		dbags.empty()
		bullets.empty()
		dude.center_dude()


def lose_round(dbags, screen, settings, stats, scoreboard, dude, bullets):
	if stats.dudes_left > 0:
		# Lose a life
		stats.dudes_left -= 1
		scoreboard.prep_dudes()
		# Delete dbags and bullets
		dbags.empty()
		bullets.empty()
		# Reset round stats
		stats.round_dbags_killed = 0
		# Put the dude back in the center
		dude.center_dude()
		# Pause
		sleep(0.5)
	else:
		# Turn the mouse cursor on
		pygame.mouse.set_visible = True
		stats.game_active = False
		stats.game_over = True
	
	
def win_round(settings, dbags, stats, dude, bullets, scoreboard):
	dbags.empty()
	bullets.empty()
	settings.increase_speed()
	stats.game_score += stats.round_num * settings.round_bonus_multi
	check_high_score(stats, scoreboard)	
	stats.round_dbags_killed = 0
	stats.round_num += 1
	scoreboard.prep_high_score()
	scoreboard.prep_score()
	scoreboard.prep_round()
	dude.center_dude()
	sleep(0.5)
	
	
