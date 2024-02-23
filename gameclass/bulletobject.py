import pygame

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/bullet.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.mask = pygame.mask.from_surface(self.image)

	def update(self):
		self.rect.y -= 15
		if self.rect.bottom < 0:
			self.kill()
