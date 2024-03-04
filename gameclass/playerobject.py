import pygame
from gameclass.bulletobject import Bullet
from math import sqrt

class Player(pygame.sprite.Sprite):
	def __init__(self, screen_info, bullet_group, black, green):
		pygame.sprite.Sprite.__init__(self)
		self.screen_width = screen_info[0]
		self.screen_height = screen_info[1]
		self.screen = screen_info[2]
		self.x = int(self.screen_width / 2) - 200
		self.y = self.screen_height - 100
		self.black = black
		self.green = green
		self.spritesheet = {
			"idle": pygame.image.load("img/player_idle.png").convert_alpha(),
			"left": pygame.image.load("img/player_left.png").convert_alpha(),
			"right": pygame.image.load("img/player_right.png").convert_alpha()
			}
		self.images = {key: [sprite.subsurface(pygame.Rect(j * 64, i * 64, 64, 64)) for i in range(1) for j in range(4)] for key, sprite in self.spritesheet.items()}
		self.current_image = 0
		self.image = self.images["idle"][self.current_image]
		self.original_image = self.image
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)
		self.original_x = self.x
		self.original_y = self.y
		self.hitbox_image = pygame.image.load("img/player_hitbox.png").convert_alpha()
		self.life_start = 3
		self.life_remaining = 3
		self.last_shot = pygame.time.get_ticks()
		self.animation_time = 0.5
		self.current_time = 0
		self.direction = "idle"
		self.bullet_group = bullet_group
		self.extra_spread_pos = 0
		self.stop_shooting = False
		self.disable_hitbox = False
		self.invincible = False
		self.last_hit_time = 0
		self.score = 0
		self.graze = 0

	def reset_position(self):
		self.rect.center = (self.original_x, self.original_y)

	def damage_and_reset(self):
		self.life_remaining -= 1
		self.reset_position()
		self.direction = "idle"
		self.invincible = True
		self.last_hit_time = pygame.time.get_ticks()

	def update(self, dt):
		speed = 12
		dx = 0
		dy = 0
		
		cooldown = 100
		bullet_spread = 35
		bullet_extra_spread = (-10, 20, 30, 20, -10)

		key = pygame.key.get_pressed()
		if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
			speed = 6
			bullet_spread = 15
			bullet_extra_spread = (0, 8, 16, 8, 0)
		
		if key[pygame.K_LEFT] and self.rect.left > 20:
			dx = -1
			if not self.invincible:
				self.direction = "left"
		elif key[pygame.K_RIGHT] and self.rect.right < self.screen_width - 410:
			dx = 1
			if not self.invincible:
				self.direction = "right"
		else:
			self.direction = "idle"
		if key[pygame.K_UP] and self.rect.top > 0:
			dy = -1
		if key[pygame.K_DOWN] and self.rect.bottom < self.screen_height:
			dy = 1

		if dx != 0 and dy != 0:
			dx /= sqrt(2)
			dy /= sqrt(2)

		self.rect.x += dx * speed
		self.rect.y += dy * speed

		time_now = pygame.time.get_ticks()
		if self.stop_shooting == False:
			bullet_spread += bullet_extra_spread[self.extra_spread_pos]
			if key[pygame.K_z] and time_now - self.last_shot > cooldown:
				bullet1 = Bullet(self.rect.centerx - bullet_spread, self.rect.top, self.screen_width)
				bullet2 = Bullet(self.rect.centerx, self.rect.top, self.screen_width)
				bullet3 = Bullet(self.rect.centerx + bullet_spread, self.rect.top, self.screen_width)
				self.bullet_group.add(bullet1)
				self.bullet_group.add(bullet2)
				self.bullet_group.add(bullet3)
				self.last_shot = time_now
				self.extra_spread_pos += 1
				if self.extra_spread_pos >= 5:
					self.extra_spread_pos = -1

		self.mask = pygame.mask.from_surface(self.hitbox_image)

		pygame.draw.rect(self.screen, self.black, (750, 190, 210, 25))
		if self.life_remaining > 0:
			pygame.draw.rect(self.screen, self.green, (750, 190, int(210 * (self.life_remaining / self.life_start)), 25))
		self.current_time += dt
		
		if self.current_time >= self.animation_time:
			self.current_time = 0
			self.current_image = (self.current_image + 1) % len(self.images[self.direction])
			self.image = self.images[self.direction][self.current_image]

class GrazingHitbox(pygame.sprite.Sprite):
	def __init__(self, player):
		self.player = player
		self.image = pygame.Surface((player.rect.width - 20, player.rect.height - 20), pygame.SRCALPHA)
		self.rect = self.image.get_rect(center = player.rect.center)
