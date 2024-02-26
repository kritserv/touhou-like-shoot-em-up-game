import pygame
from math import cos, sin

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, x, y, angle, screen_width, screen_height):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/enemy_bullet.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.mask = pygame.mask.from_surface(self.image)
		self.grazed = False
		self.speed = 10
		self.vx = self.speed * cos(angle)
		self.vy = self.speed * sin(angle)
		self.screen_width = screen_width
		self.screen_height = screen_height

	def update(self):	    
		self.rect.y += self.vy
		self.rect.x += self.vx
		if self.rect.top > self.screen_height or self.rect.bottom < 0 or self.rect.x < 20 or self.rect.x > self.screen_width - 435:
			self.kill()
