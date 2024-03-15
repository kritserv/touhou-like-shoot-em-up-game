import pygame
from math import cos, sin, atan2, pi
from object.timer import Timer

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, x, y, angle, speed, slow_speed, screen_width, screen_height, focus_player, style, slow_at_center, bounce_top):
		pygame.sprite.Sprite.__init__(self)
		self.style = style
		if self.style == 1:
			self.original_image = pygame.image.load("asset/img/enemy_bullet.png").convert_alpha()
			self.image = pygame.transform.rotate(self.original_image, -angle * 180 / pi)
		else:
			self.image = pygame.image.load("asset/img/enemy_bullet_round.png").convert_alpha()
		self.rect = self.image.get_rect(center = (x, y))
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.mask = pygame.mask.from_surface(self.image)
		self.grazed = False
		self.speed = speed
		self.slow_speed = slow_speed
		self.angle = angle
		self.slow_at_center = slow_at_center
		self.slowed = False
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.focus_player = focus_player
		self.direction_updated = False
		self.target_delay_timer = Timer()
		self.target_delay_timer.start()
		if bounce_top:
			self.bounced = False
		else:
			self.bounced = True
		self.vx = 0
		self.vy = 0

	def toggle_pause_timer(self):
		self.target_delay_timer.toggle_pause()

	def set_target(self, target_x, target_y, delay):
		self.target_x = target_x
		self.target_y = target_y
		self.delay = delay
		self.create_time = self.target_delay_timer.get_elapsed_time()

	def focus_on_player(self):
		if self.target_delay_timer.get_elapsed_time() - self.create_time > self.delay and not self.direction_updated:
			dx = self.target_x - self.rect.centerx
			dy = self.target_y - self.rect.centery
			self.angle = atan2(dy, dx)
			if self.style == 1:
				self.image = pygame.transform.rotate(self.original_image, -self.angle * 180 / pi)
			self.vx = self.speed * cos(self.angle)
			self.vy = self.speed * sin(self.angle)
			self.direction_updated = True

	def move(self, dt):
		self.vx = self.speed * cos(self.angle)
		self.vy = self.speed * sin(self.angle)
		self.pos.y += self.vy * dt
		self.rect.y = round(self.pos.y)
		self.pos.x += self.vx * dt
		self.rect.x = round(self.pos.x)

	def bounce(self):
		self.vx = -self.vx
		self.vy = -self.vy
		self.angle = -self.angle
		if self.style == 1:
			self.image = pygame.transform.rotate(self.original_image, -self.angle * 180 / pi)

	def hit_bottom_border(self):
		return self.rect.top > self.screen_height

	def hit_top_border(self):
		return self.rect.bottom < 0

	def hit_left_border(self):
		return self.rect.left < 12

	def hit_right_border(self):
		return self.rect.right > self.screen_width - 395

	def slow_down_at_center(self):
		if self.slow_at_center:
			if self.rect.centery > self.screen_height / 2:
				self.speed = self.slow_speed
				self.slowed = True

	def update(self, dt):
		if self.hit_top_border():
			if not self.bounced:
				self.bounce()
				self.bounced = True
			else:
				self.kill()

		if self.hit_left_border() or self.hit_right_border() or self.hit_bottom_border():
			self.kill()

		if not self.slowed:
			self.slow_down_at_center()

		self.move(dt)

		if self.focus_player:
			self.focus_on_player()