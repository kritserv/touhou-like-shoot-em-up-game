import pygame
from math import cos, sin, atan2, pi
from gameclass.timerobject import Timer

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, x, y, angle, screen_width, screen_height, focus_player, style):
		pygame.sprite.Sprite.__init__(self)
		self.style = style
		if self.style == 1:
			self.original_image = pygame.image.load("gameasset/img/enemy_bullet.png").convert_alpha()
			self.image = pygame.transform.rotate(self.original_image, -angle * 180 / pi)
		else:
			self.image = pygame.image.load("gameasset/img/enemy_bullet_round.png").convert_alpha()
		self.rect = self.image.get_rect(center = (x, y))
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.mask = pygame.mask.from_surface(self.image)
		self.grazed = False
		self.speed = 500
		self.vx = self.speed * cos(angle)
		self.vy = self.speed * sin(angle)
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.focus_player = focus_player
		self.direction_updated = False
		self.target_delay_timer = Timer()
		self.target_delay_timer.start()

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
			angle = atan2(dy, dx)
			if self.style == 1:
				self.image = pygame.transform.rotate(self.original_image, -angle * 180 / pi)
			self.vx = self.speed * cos(angle)
			self.vy = self.speed * sin(angle)
			self.direction_updated = True

	def move(self, dt):
		self.pos.y += self.vy * dt
		self.rect.y = round(self.pos.y)
		self.pos.x += self.vx * dt
		self.rect.x = round(self.pos.x)

	def update(self, dt):
		self.move(dt)

		if self.rect.top > self.screen_height or self.rect.bottom < 0 or self.rect.left < 12 or self.rect.right > self.screen_width - 395:
			self.kill()

		if self.focus_player:
			self.focus_on_player()