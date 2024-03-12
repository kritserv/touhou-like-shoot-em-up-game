import pygame
from gameclass.enemybulletobject import EnemyBullet
from math import pi
from gameclass.timerobject import Timer

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
			"idle": pygame.image.load("gameasset/img/enemy_idle.png").convert_alpha(),
			"left": pygame.image.load("gameasset/img/enemy_left.png").convert_alpha(),
			"right": pygame.image.load("gameasset/img/enemy_right.png").convert_alpha()
			}
		self.shooting_sound = pygame.mixer.Sound("gameasset/soundeffect/enemy_shoot.wav")
		self.shooting_sound.set_volume(0.05)
		self.damaged_sound = pygame.mixer.Sound("gameasset/soundeffect/enemy_damaged.wav")
		self.damaged_sound.set_volume(0.07)
		self.death_sound = pygame.mixer.Sound("gameasset/soundeffect/enemy_death.wav")
		self.death_sound.set_volume(0.07)
		self.images = {key: [sprite.subsurface(pygame.Rect(j * 72, i * 88, 72, 88)) for i in range(1) for j in range(4)] for key, sprite in self.spritesheet.items()}
		self.current_image = 0
		self.image = self.images["idle"][self.current_image]
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.health_start = 500
		self.health_remaining = 500
		self.speed = 50
		self.shoot_timer = Timer()
		self.shoot_timer.start()
		self.bullet_delay = 0.3
		self.bullet_spiral_delay = 0.05
		self.last_bullet_time = self.shoot_timer.get_elapsed_time()
		self.bullet_index = 0
		self.animation_time = 0.1
		self.current_frame = 0
		self.current_time = 0
		self.direction = "idle"
		self.stop_shooting = False
		self.enemybullet_group = enemybullet_group

	def restart_timer(self):
		self.shoot_timer.restart()
		self.last_bullet_time = self.shoot_timer.get_elapsed_time()

	def pause_timer(self):
		self.shoot_timer.pause()

	def resume_timer(self):
		self.shoot_timer.resume()

	def toggle_pause_timer(self):
		self.shoot_timer.toggle_pause()

	def normal_shoot(self, focus_player, player, delay_before_focus, style):
		self.current_time = self.shoot_timer.get_elapsed_time()
		if self.current_time - self.last_bullet_time > self.bullet_delay and self.stop_shooting == False:
			self.shooting_sound.play()
			self.last_bullet_time = self.current_time
			bullet = EnemyBullet(self.rect.centerx, self.rect.centery, pi / 2, self.screen_width, self.screen_height, focus_player, style)
			if focus_player:
				bullet.set_target(player.rect.centerx, player.rect.centery, delay_before_focus)
			self.enemybullet_group.add(bullet)

	def circular_shoot(self, amount, focus_player, player, delay_before_focus, style):
		self.current_time = self.shoot_timer.get_elapsed_time()
		if self.current_time - self.last_bullet_time > self.bullet_delay and self.stop_shooting == False:
			self.shooting_sound.play()
			self.last_bullet_time = self.current_time
			for i in range(amount):
				angle = 2 * pi * i / amount
				bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle, self.screen_width, self.screen_height, focus_player, style)
				if focus_player:
					bullet.set_target(player.rect.centerx, player.rect.centery, delay_before_focus)
				self.enemybullet_group.add(bullet)

	def spiral_shoot(self, amount, focus_player, player, delay_before_focus, style):
		self.current_time = self.shoot_timer.get_elapsed_time()
		if self.current_time - self.last_bullet_time > self.bullet_spiral_delay:
			self.shooting_sound.play()
			self.last_bullet_time = self.current_time
			angle = 2 * pi * self.bullet_index / amount
			bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle, self.screen_width, self.screen_height, focus_player, style)
			if focus_player:
				bullet.set_target(player.rect.centerx, player.rect.centery, delay_before_focus)
			self.enemybullet_group.add(bullet)
			self.bullet_index = (self.bullet_index + 1) % amount

	def spiral_shoot_2(self, amount, focus_player, player, delay_before_focus, style):
		self.current_time = self.shoot_timer.get_elapsed_time()
		if self.current_time - self.last_bullet_time > self.bullet_spiral_delay:
			self.shooting_sound.play()
			self.last_bullet_time = self.current_time
			angle = 2 * pi * self.bullet_index / amount
			bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle, self.screen_width, self.screen_height, focus_player, style)
			if focus_player:
				bullet.set_target(player.rect.centerx, player.rect.centery, delay_before_focus)
			self.enemybullet_group.add(bullet)
			another_bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle + pi, self.screen_width, self.screen_height, focus_player, style)
			if focus_player:
				another_bullet.set_target(player.rect.centerx, player.rect.centery, delay_before_focus)
			self.enemybullet_group.add(another_bullet)
			self.bullet_index = (self.bullet_index + 1) % amount

	def move_left(self, dt):
		self.pos.x  += -1 * self.speed * dt
		self.rect.x = round(self.pos.x)

	def move_right(self, dt):
		self.pos.x  += 1 * self.speed * dt
		self.rect.x = round(self.pos.x)

	def move_up(self, dt):
		self.pos.y  += -1 * self.speed * dt
		self.rect.y = round(self.pos.y)

	def move_down(self, dt):
		self.pos.y  += 1 * self.speed * dt
		self.rect.y = round(self.pos.y)

	def move_mask(self):
		self.mask = pygame.mask.from_surface(self.image)

	def reset_position(self):
		self.rect.center = (self.x, self.y)
		self.pos = pygame.math.Vector2(self.rect.topleft)

	def draw_health_bar(self):
		pygame.draw.rect(self.screen, self.black, (55, 20, 530, 15))
		if self.health_remaining > 0:
			pygame.draw.rect(self.screen, self.red, (55, 20, int(530 * (self.health_remaining / self.health_start)), 15))

	def animate(self, dt):
		self.current_frame += dt
		if self.current_frame >= self.animation_time:
			self.current_frame -= self.animation_time
			self.current_image = (self.current_image + 1) % len(self.images[self.direction])
			self.image = self.images[self.direction][self.current_image]

	def update(self, dt):
		self.animate(dt)
		self.move_mask()