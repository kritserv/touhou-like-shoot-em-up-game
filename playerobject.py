import pygame

screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))

red = (255, 0, 0)
green = (0, 255, 0)

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, health):
		pygame.sprite.Sprite.__init__(self)
		self.spritesheet = {
			"idle": pygame.image.load("img/player_idle.png"),
			"left": pygame.image.load("img/player_left.png"),
			"right": pygame.image.load("img/player_right.png")
			}
		self.images = {key: [sprite.subsurface(pygame.Rect(j * 64, i * 64, 64, 64)) for i in range(1) for j in range(4)] for key, sprite in self.spritesheet.items()}
		self.current_image = 0
		self.image = self.images["idle"][self.current_image]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.health_start = health
		self.health_remaining = health
		self.animation_time = 0.5
		self.current_time = 0
		self.direction = "idle"

	def update(self, dt):
		speed = 10
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > 20:
			self.rect.x -= speed
			self.direction = "left"
		elif key[pygame.K_RIGHT] and self.rect.right < screen_width - 400:
			self.rect.x += speed
			self.direction = "right"
		else:
			self.direction = "idle"
		if key[pygame.K_UP] and self.rect.top > 0:
			self.rect.y -= speed
		if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
			self.rect.y += speed

		pygame.draw.rect(screen, red, (700, 200, 250, 35))
		if self.health_remaining > 0:
			pygame.draw.rect(screen, green, (700, 200, int(250 * (self.health_remaining / self.health_start)), 35))

		self.current_time += dt
		if self.current_time >= self.animation_time:
			self.current_time = 0
			self.current_image = (self.current_image + 1) % len(self.images[self.direction])
			self.image = self.images[self.direction][self.current_image]