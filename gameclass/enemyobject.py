import pygame

screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))

black = (0, 0, 0)
red = (255, 0, 0)

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y, health, bullet_group):
		pygame.sprite.Sprite.__init__(self)
		self.spritesheet = {
			"idle": pygame.image.load("img/enemy_idle.png"),
			"left": pygame.image.load("img/enemy_left.png"),
			"right": pygame.image.load("img/enemy_right.png")
			}
		self.images = {key: [sprite.subsurface(pygame.Rect(j * 72, i * 88, 72, 88)) for i in range(1) for j in range(4)] for key, sprite in self.spritesheet.items()}
		self.current_image = 0
		self.image = self.images["idle"][self.current_image]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.health_start = health
		self.health_remaining = health
		self.last_shot = pygame.time.get_ticks()
		self.animation_time = 0.5
		self.current_time = 0
		self.direction = "idle"
		self.bullet_group = bullet_group

	def update(self, dt):
		speed = 10

		pygame.draw.rect(screen, black, (55, 20, 530, 15))
		if self.health_remaining > 0:
			pygame.draw.rect(screen, red, (55, 20, int(530 * (self.health_remaining / self.health_start)), 15))

		self.current_time += dt
		if self.current_time >= self.animation_time:
			self.current_time = 0
			self.current_image = (self.current_image + 1) % len(self.images[self.direction])
			self.image = self.images[self.direction][self.current_image]

		self.mask = pygame.mask.from_surface(self.image)
