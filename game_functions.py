import sys
import pygame
from pygame.sprite import Group
from bullet import Bullet
from dbag import Dbag
from time import sleep

def check_events(settings, screen, stats, dbags, dude, bullets, play_button, scoreboard):
	# Checking for events coming in
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, settings, screen, stats, dude, dbags, bullets, scoreboard)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, dude)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(settings, screen, stats, dbags, dude, bullets, play_button, scoreboard, mouse_x, mouse_y)

def check_keydown_events(event, settings, screen, stats, dude, dbags, bullets, scoreboard):
	# Check keys being pressed and assign actions
	if event.key == pygame.K_d:
		dude.moving_right = True
	elif event.key == pygame.K_a:
		dude.moving_left = True
	elif event.key == pygame.K_w:
		dude.moving_up = True
	elif event.key == pygame.K_s:
		dude.moving_down = True
	elif event.key == pygame.K_LEFT and len(bullets) < settings.bullet_max_num:
		# Spawn new bullet, add it to the Group
		new_bullet = Bullet(settings, screen, dude, trajectory='left')
		bullets.add(new_bullet)
	elif event.key == pygame.K_UP and len(bullets) < settings.bullet_max_num:
		# Spawn new bullet, add it to the Group
		new_bullet = Bullet(settings, screen, dude, trajectory='up')
		bullets.add(new_bullet)	
	elif event.key == pygame.K_RIGHT and len(bullets) < settings.bullet_max_num:
		# Spawn new bullet, add it to the Group
		new_bullet = Bullet(settings, screen, dude, trajectory='right')
		bullets.add(new_bullet)
	elif event.key == pygame.K_DOWN and len(bullets) < settings.bullet_max_num:
		# Spawn new bullet, add it to the Group
		new_bullet = Bullet(settings, screen, dude, trajectory='down')
		bullets.add(new_bullet)
	elif not stats.game_active and event.key == pygame.K_p:
		start_game(settings, stats, dbags, bullets, dude, scoreboard)
	elif event.key == 27:
		sys.exit()
		
		
def check_keyup_events(event, dude):
	# Check keys being released and assign actions
	if event.key == pygame.K_d:
		dude.moving_right = False
	elif event.key == pygame.K_a:
		dude.moving_left = False
	elif event.key == pygame.K_w:
		dude.moving_up = False
	elif event.key == pygame.K_s:
		dude.moving_down = False
		
		
def check_play_button(settings, screen, stats, dbags, dude, bullets, play_button, scoreboard, mouse_x, mouse_y):
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		start_game(settings, stats, dbags, bullets, dude, scoreboard)


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
	
	
