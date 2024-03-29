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
			style = 1, 
			speed = 500, 
			changed_speed = 220, 
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
			speed = 250, 
			changed_speed = None, 
			change_speed_at_center = False, 
			bounce_top = True)
		self.enemy.move_up(dt)

	def pattern_2(self, dt):
		self.set_shoot_delay(0.05)
		self.enemy.normal_shoot(focus_player = False, 
			player = self.player, 
			delay_before_focus = 0, 
			style = 1, 
			speed = 450, 
			changed_speed = 0, 
			change_speed_at_center = False, 
			bounce_top = False)

	def pattern_3(self, dt):
		self.set_shoot_delay(0.05)
		self.enemy.circular_shoot(amount = 14, 
			focus_player = False, 
			player = self.player, 
			delay_before_focus = 0, 
			style = 1, 
			speed = 220, 
			changed_speed = 190, 
			change_speed_at_center = True, 
			bounce_top = False)

	def pattern_4(self, dt):
		self.set_shoot_delay(0.5)
		self.enemy.circular_shoot(amount = 24, 
			focus_player = False, 
			player = self.player, 
			delay_before_focus = 0, 
			style = 0, 
			speed = 320, 
			changed_speed = 190, 
			change_speed_at_center = True, 
			bounce_top = True)

	def pattern_5(self, dt):
		self.set_shoot_delay(0.2)
		self.enemy.spiral_shoot_2(amount = 90, 
			focus_player = False, 
			player = self.player, 
			delay_before_focus = 0, 
			style = 1, 
			speed = 320, 
			changed_speed = 150, 
			change_speed_at_center = True, 
			bounce_top = True)

	def pattern_6(self, dt):
		self.set_shoot_delay(0.15)
		self.enemy.spiral_shoot_2(amount = 75, 
			focus_player = True, 
			player = self.player, 
			delay_before_focus = 1.0, 
			style = 1, 
			speed = 320, 
			changed_speed = 250, 
			change_speed_at_center = True, 
			bounce_top = False)

	def pattern_7(self, dt):
		self.set_shoot_delay(0.5)
		self.enemy.circular_shoot(amount = 37, 
			focus_player = False, 
			player = self.player, 
			delay_before_focus = 0, 
			style = 0, 
			speed = 210, 
			changed_speed = 0, 
			change_speed_at_center = False, 
			bounce_top = True)

	def phase_1(self, dt, current_time):
		if 0 <= current_time < 5.0:
			self.enemy.direction = "idle"
			self.pattern_7(dt)
		elif 5.0 <= current_time < 8.0:
			self.enemy.speed = 50
			self.pattern_0(dt)
			self.enemy.move_left(dt)
			self.enemy.direction = "left"
		elif 8.0 <= current_time < 9.0:
			self.enemy.speed = 180
			self.enemy.move_right(dt)
			self.enemy.direction = "right"
		elif 9.0 <= current_time < 12.0:
			self.enemy.speed = 50
			self.pattern_1(dt)
			self.enemy.move_right(dt)
			self.enemy.direction = "right"
		elif 12.0 <= current_time < 14.2:
			self.enemy.direction = "idle"
		elif 14.2 <= current_time < 15.2:
			self.enemy.speed = 180
			self.enemy.move_left(dt)
			self.enemy.direction = "left"
		else:
			self.restart_timer()

	def phase_2(self, dt, current_time):
		if 0 <= current_time < 0.2:
			self.enemy.speed = 400
			self.enemy.move_left(dt)
			self.enemy.direction = "left"
		elif 0.2 <= current_time < 0.4:
			self.enemy.direction = "idle"
			self.pattern_3(dt)
		elif 0.4 <= current_time < 0.6:
			self.enemy.move_left(dt)
			self.enemy.direction = "left"
		elif 0.6 <= current_time < 0.8:
			self.enemy.direction = "idle"
			self.pattern_3(dt)
		elif 0.8 <= current_time < 1.0:
			self.enemy.speed = 800
			self.enemy.move_right(dt)
			self.enemy.direction = "right"
		elif 1.0 <= current_time < 1.2:
			self.enemy.speed = 400
			self.enemy.direction = "idle"
			self.pattern_3(dt)
		elif 1.2 <= current_time < 1.4:
			self.enemy.direction = "right"
			self.enemy.move_right(dt)
		elif 1.4 <= current_time < 1.6:
			self.enemy.direction = "idle"
		elif 1.6 <= current_time < 1.8:
			self.enemy.direction = "left"
			self.enemy.move_left(dt)
			self.pattern_2(dt)
		elif 1.8 <= current_time < 2.2:
			self.enemy.direction = "idle"
			self.pattern_2(dt)
		elif 2.2 <= current_time < 3.0:
			self.pattern_3(dt)
			self.enemy.direction = "right"
			self.enemy.move_right(dt)
			self.enemy.move_down(dt)
		elif 3.0 <= current_time < 4.5:
			self.enemy.direction = "idle"
		elif 4.5 <= current_time < 5.3:
			self.pattern_3(dt)
			self.enemy.direction = "left"
			self.enemy.move_left(dt)
			self.enemy.move_up(dt)
		elif 5.3 <= current_time < 6.5:
			self.enemy.direction = "idle"
		elif 6.5 <= current_time < 8.5:
			self.enemy.direction = "idle"
			self.pattern_4(dt)
		elif 8.5 <= current_time < 10.0:
			self.enemy.direction = "idle"
		elif 10.0 <= current_time < 14.0:
			self.enemy.direction = "idle"
			self.pattern_5(dt)
		elif 14.0 <= current_time < 16.0:
			self.enemy.direction = "idle"
		else:
			self.restart_timer()

	def phase_3(self, dt, current_time):
		if 0 <= current_time < 0.2:
			self.enemy.speed = 120
			self.enemy.move_right(dt)
			self.enemy.move_down(dt)
			self.enemy.direction = "right"
		elif 0.2 <= current_time < 1.0:
			self.enemy.speed = 20
			self.enemy.direction = "idle"
			self.enemy.move_up(dt)
			self.pattern_7(dt)
		elif 1.0 <= current_time < 5.0:
			self.enemy.direction = "idle"
			self.pattern_6(dt)
		elif 5.0 <= current_time < 5.2:
			self.enemy.speed = 120
			self.enemy.move_up(dt)
			self.enemy.move_left(dt)
			self.enemy.direction = "left"
		elif 5.2 <= current_time < 6.0:
			self.enemy.speed = 20
			self.enemy.move_down(dt)
			self.enemy.direction = "idle"
		elif 6.0 <= current_time < 8.0:
			self.enemy.direction = "idle"
		elif 8.0 <= current_time < 9.0:
			self.enemy.speed = 170
			self.enemy.move_left(dt)
			self.enemy.move_down(dt)
			self.enemy.direction = "left"
			self.pattern_2(dt)
		elif 9.0 <= current_time < 12.0:
			self.enemy.direction = "idle"
			self.pattern_7(dt)
		elif 12.0 <= current_time < 13.0:
			self.enemy.move_right(dt)
			self.enemy.move_up(dt)
			self.enemy.direction = "right"
			self.pattern_2(dt)
		elif 13.0 <= current_time < 15.0:
			self.enemy.direction = "idle"
		else:
			self.restart_timer()

	def play_again(self):
		self.restart_timer()

	def update(self, dt):
		if not self.enemy.stop_shooting:
			current_time = self.timer.get_elapsed_time()
			if self.enemy.life_remaining == 2:
				self.phase_1(dt, current_time)
			elif self.enemy.life_remaining == 1:
				self.phase_2(dt, current_time)
			else:
				self.phase_3(dt, current_time)