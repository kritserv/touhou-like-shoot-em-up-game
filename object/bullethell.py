from object.timer import Timer

class BulletHell:
	def __init__(self, enemy, player):
		self.enemy = enemy
		self.player = player
		self.timer = Timer()

	def start_timer(self):
		self.timer.start_or_resume()

	def restart_timer(self):
		self.timer.restart()

	def pause_timer(self):
		self.timer.pause()

	def toggle_pause_timer(self):
		self.timer.toggle_pause()

	def set_shoot_delay(self, value):
		self.enemy.bullet_delay = value
		self.enemy.bullet_spiral_delay = value * 0.1

	def pattern_0(self, dt):
		self.set_shoot_delay(0.9)
		self.enemy.circular_shoot(amount = 20, 
			focus_player = False, 
			player = self.player, 
			delay_before_focus = 0, 
			style = 0, 
			speed = 500, 
			changed_speed = 380, 
			change_speed_at_center = True, 
			bounce_top = True)
		self.enemy.move_down(dt)

	def pattern_1(self, dt):
		self.set_shoot_delay(0.2)
		self.enemy.spiral_shoot(amount = 30, 
			focus_player = True, 
			player = self.player, 
			delay_before_focus = 0.5, 
			style = 1, 
			speed = 450, 
			changed_speed = None, 
			change_speed_at_center = False, 
			bounce_top = True)
		self.enemy.move_up(dt)

	def play_again(self):
		self.restart_timer()

	def update(self, dt):
		if not self.enemy.stop_shooting:
			current_time = self.timer.get_elapsed_time()
			if 0 <= current_time < 1:
				self.enemy.move_left(dt)
				self.enemy.direction = "left"
			elif 1 <= current_time < 4:
				self.pattern_0(dt)
				self.enemy.direction = "idle"
			elif 4 <= current_time < 5:
				self.enemy.move_right(dt)
				self.enemy.direction = "right"
			elif 5 <= current_time < 8:
				self.pattern_1(dt)
				self.enemy.direction = "idle"
			else:
				self.restart_timer()