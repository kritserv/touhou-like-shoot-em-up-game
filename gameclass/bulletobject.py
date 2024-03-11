import pygame

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, screen_width):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("gameasset/img/bullet.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.mask = pygame.mask.from_surface(self.image)
		self.screen_width = screen_width

	def move(self, dt):
		self.pos.y -= 900 * dt
		self.rect.y = round(self.pos.y)

	def update(self, dt):
		self.move(dt)
		if self.rect.bottom < 0 or self.rect.x < 20 or self.rect.x > self.screen_width - 415:
			self.kill()
