import pygame
from gameclass.enemybulletobject import EnemyBullet
from math import pi
    
class Enemy(pygame.sprite.Sprite):
	def __init__(self, screen_info, enemybullet_group, black, red):
		pygame.sprite.Sprite.__init__(self)
		self.screen_width = screen_info[0]
		self.screen_height = screen_info[1]
		self.screen = screen_info[2]
		self.x = int(self.screen_width / 2) - 200
		self.y = self.screen_height - 600
		self.black = black
		self.red = red
		self.spritesheet = {
			"idle": pygame.image.load("img/enemy_idle.png"),
			"left": pygame.image.load("img/enemy_left.png"),
			"right": pygame.image.load("img/enemy_right.png")
			}
		self.images = {key: [sprite.subsurface(pygame.Rect(j * 72, i * 88, 72, 88)) for i in range(1) for j in range(4)] for key, sprite in self.spritesheet.items()}
		self.current_image = 0
		self.image = self.images["idle"][self.current_image]
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)
		self.health_start = 500
		self.health_remaining = 500
		self.last_shot = pygame.time.get_ticks()
		self.bullet_delay = 300
		self.bullet_spiral_delay = 1
		self.last_bullet_time = pygame.time.get_ticks()
		self.bullet_index = 0
		self.animation_time = 0.5
		self.current_time = 0
		self.direction = "idle"
		self.stop_shooting = False
		self.enemybullet_group = enemybullet_group
		
	def normal_shoot(self):
	    current_time = pygame.time.get_ticks()
	    if current_time - self.last_bullet_time > self.bullet_delay and self.stop_shooting == False:
	    	self.last_bullet_time = current_time
	    	bullet = EnemyBullet(self.rect.centerx, self.rect.centery, pi / 2, self.screen_width, self.screen_height)
	    	self.enemybullet_group.add(bullet)

	def circular_shoot(self):
	    amount = 32
	    current_time = pygame.time.get_ticks()
	    if current_time - self.last_bullet_time > self.bullet_delay and self.stop_shooting == False:
	    	self.last_bullet_time = current_time
	    	for i in range(amount):
	    	    angle = 2 * pi * i / amount
	    	    bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle, self.screen_width, self.screen_height)
	    	    self.enemybullet_group.add(bullet)

	def spiral_shoot(self):
	    amount = 32
	    current_time = pygame.time.get_ticks()
	    if current_time - self.last_bullet_time > self.bullet_spiral_delay:
	    	self.last_bullet_time = current_time
	    	angle = 2 * pi * self.bullet_index / amount
	    	bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle, self.screen_width, self.screen_height)
	    	self.enemybullet_group.add(bullet)
	    	self.bullet_index = (self.bullet_index + 1) % amount

	def update(self, dt):
		speed = 10

		pygame.draw.rect(self.screen, self.black, (55, 20, 530, 15))
		if self.health_remaining > 0:
			pygame.draw.rect(self.screen, self.red, (55, 20, int(530 * (self.health_remaining / self.health_start)), 15))

		self.current_time += dt
		if self.current_time >= self.animation_time:
			self.current_time = 0
			self.current_image = (self.current_image + 1) % len(self.images[self.direction])
			self.image = self.images[self.direction][self.current_image]

		self.mask = pygame.mask.from_surface(self.image)
