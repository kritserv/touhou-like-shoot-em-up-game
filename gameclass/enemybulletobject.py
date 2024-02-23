import pygame

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/enemy_bullet.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.mask = pygame.mask.from_surface(self.image)

	def update(self):
		self.rect.y += 10
		screen_height = 768
		if self.rect.top > screen_height:
			self.kill()
