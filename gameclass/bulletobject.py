import pygame

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, screen_width):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("img/bullet.png")
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.mask = pygame.mask.from_surface(self.image)
		self.screen_width = screen_width

	def update(self):
		self.rect.y -= 45
		if self.rect.bottom < 0 or self.rect.x < 20 or self.rect.x > self.screen_width - 415:
			self.kill()
