import pygame
from math import cos, sin, pi

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, x, y, angle, screen_width, screen_height):
		pygame.sprite.Sprite.__init__(self)
		self.original_image = pygame.image.load("img/enemy_bullet.png")
		self.image = pygame.transform.rotate(self.original_image, -angle * 180 / pi)
		self.rect = self.image.get_rect(center = (x, y))
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
		if self.rect.top > self.screen_height or self.rect.bottom < 0 or self.rect.left < 12 or self.rect.right > self.screen_width - 395:
			self.kill()
