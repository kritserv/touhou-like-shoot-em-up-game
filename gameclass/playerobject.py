import pygame
from gameclass.bulletobject import Bullet

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
			"idle": pygame.image.load("img/player_idle.png"),
			"left": pygame.image.load("img/player_left.png"),
			"right": pygame.image.load("img/player_right.png")
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
		self.health_start = 3
		self.health_remaining = 3
		self.last_shot = pygame.time.get_ticks()
		self.animation_time = 0.5
		self.current_time = 0
		self.direction = "idle"
		self.bullet_group = bullet_group
		self.stop_shooting = False
		self.invincible = False
		self.last_hit_time = 0
		self.score = 0
		self.graze = 0

	def reset(self):
		self.rect.center = (self.original_x, self.original_y)
		self.invincible = True
		self.last_hit_time = pygame.time.get_ticks()

	def update(self, dt):
		speed = 12
		cooldown = 100
		bullet_spread = 45

		key = pygame.key.get_pressed()
		if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
			speed = 6
			bullet_spread = 15
		
		if key[pygame.K_LEFT] and self.rect.left > 20:
			self.rect.x -= speed
			if not self.invincible:
			    self.direction = "left"
		elif key[pygame.K_RIGHT] and self.rect.right < self.screen_width - 410:
			self.rect.x += speed
			if not self.invincible:
			    self.direction = "right"
		else:
			self.direction = "idle"
		if key[pygame.K_UP] and self.rect.top > 0:
			self.rect.y -= speed
		if key[pygame.K_DOWN] and self.rect.bottom < self.screen_height:
			self.rect.y += speed

		time_now = pygame.time.get_ticks()
		if self.stop_shooting == False:
			if key[pygame.K_z] and time_now - self.last_shot > cooldown:
			    bullet1 = Bullet(self.rect.centerx - bullet_spread, self.rect.top)
			    bullet2 = Bullet(self.rect.centerx, self.rect.top)
			    bullet3 = Bullet(self.rect.centerx + bullet_spread, self.rect.top)
			    self.bullet_group.add(bullet1)
			    self.bullet_group.add(bullet2)
			    self.bullet_group.add(bullet3)
			    self.last_shot = time_now

		self.mask = pygame.mask.from_surface(self.hitbox_image)

		pygame.draw.rect(self.screen, self.black, (750, 190, 210, 25))
		if self.health_remaining > 0:
		    pygame.draw.rect(self.screen, self.green, (750, 190, int(210 * (self.health_remaining / self.health_start)), 25))
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
