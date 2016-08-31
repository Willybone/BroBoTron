class GameStats():
	def __init__ (self, settings):
		self.settings = settings
		self.reset_stats()

		# High score info
		self.high_score = 0
		
	def reset_stats(self):
		self.game_active = False
		self.dudes_left = self.settings.dude_num_lives
		self.round_num = 1
		self.game_score = 0
		self.round_dbags_killed = 0
		
