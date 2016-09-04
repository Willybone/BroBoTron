class Settings():
	# Stores all the settings for the game
	def __init__(self):
		# Assigning values to settings
		self.screen_width = 900
		self.screen_height = 700
		self.bg_color = (0, 0, 0)
		
		# Dude settings
		self.dude_num_lives = 2
		
		# Bullet settings
		self.bullet_wide = 3
		self.bullet_long = 20
		self.bullet_color = (241, 108, 4)
		self.bullet_max_num = 5
		self.bullet_rate = 35
		
		# Dbag settings
		self.dbag_starting_num = 3
		self.dbag_max_steps = 150
		self.dbag_points = 10
		
		# Round settings
		self.round_score_increase = 1.5
		self.round_speed_increase = 0.05
		self.round_dbag_increase = 10
		self.round_dbag_wave_increase = 1
		self.round_bonus_multi = 100
		
		# Game speed settings
		self.speedup_scale = 1.1
		# Game score scale
		self.score_scale = 1.5
		
		# Set starting score and speed stats
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		self.dude_speed_factor = 1
		self.dbag_speed_factor = .1
		self.bullet_speed_factor = 2.5
		
	def increase_speed(self):
		self.dude_speed_factor *= self.speedup_scale
		self.dbag_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.dbag_points *= self.score_scale
