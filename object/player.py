import pygame
from object.playerbullet import PlayerBullet
from object.timer import Timer
from math import sqrt

class Player(pygame.sprite.Sprite):
	def __init__(self, screen_info, playerbullet_group, black, green):
		pygame.sprite.Sprite.__init__(self)
		self.screen_width = screen_info[0]
		self.screen_height = screen_info[1]
		self.screen = screen_info[2]
		self.x = int(self.screen_width / 2) - 200
		self.y = self.screen_height - 100
		self.black = black
		self.green = green
		self.spritesheet = {
			"idle": pygame.image.load("asset/img/player_idle.png").convert_alpha(),
			"left": pygame.image.load("asset/img/player_left.png").convert_alpha(),
			"right": pygame.image.load("asset/img/player_right.png").convert_alpha()
			}
		self.hitbox_image = pygame.image.load("asset/img/player_hitbox.png").convert_alpha()
		self.shooting_sound = pygame.mixer.Sound("asset/soundeffect/player_shoot.wav")
		self.shooting_sound.set_volume(0.06)
		self.damaged_sound = pygame.mixer.Sound("asset/soundeffect/player_damaged.wav")
		self.damaged_sound.set_volume(0.07)
		self.pickup_sound = pygame.mixer.Sound("asset/soundeffect/player_pickup.wav")
		self.pickup_sound.set_volume(0.07)
		self.images = {key: [sprite.subsurface(pygame.Rect(j * 64, i * 64, 64, 64)) for i in range(1) for j in range(4)] for key, sprite in self.spritesheet.items()}
		self.current_image = 0
		self.image = self.images["idle"][self.current_image]
		self.original_image = self.image
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.original_x = self.x
		self.original_y = self.y
		self.life_start = 3
		self.life_remaining = 3
		self.power = 1.00
		self.animation_time = 0.1
		self.current_frame = 0
		self.direction = "idle"
		self.playerbullet_group = playerbullet_group
		self.extra_spread_pos = 0
		self.stop_shooting = False
		self.disable_hitbox = False
		self.show_hitbox = False
		self.invincible = False
		self.score = 0
		self.graze = 0
		self.shoot_timer = Timer()
		self.invincible_timer = Timer()

	def start_timer(self):
		self.shoot_timer.start()
		self.invincible_timer.start()

	def restart_timer(self):
		self.shoot_timer.restart()
		self.invincible_timer.restart()

	def pause_timer(self):
		self.shoot_timer.pause()
		self.invincible_timer.pause()

	def resume_timer(self):
		self.shoot_timer.resume()
		self.invincible_timer.resume()

	def toggle_pause_timer(self):
		self.shoot_timer.toggle_pause()
		self.invincible_timer.toggle_pause()

	def reset_position(self):
		self.rect.center = (self.original_x, self.original_y)
		self.pos = pygame.math.Vector2(self.rect.topleft)

	def damage_and_reset(self):
		self.damaged_sound.play()
		self.life_remaining -= 1
		self.reset_position()
		self.direction = "idle"
		self.invincible = True
		self.last_hit_time = self.invincible_timer.get_elapsed_time()

	def draw_hitbox(self):
	    if not self.disable_hitbox:
	        hitbox_position = self.rect.topleft
	        self.screen.blit(self.hitbox_image, hitbox_position)

	def make_transparent(self):
	    if self.invincible_timer.get_elapsed_time() - self.last_hit_time <= 2:
	        temp_image = self.original_image.copy()
	        temp_image.set_alpha(128)
	        self.image = temp_image
	    else:
	        self.image = self.original_image
	        self.invincible = False
	        self.image.set_alpha(255)

	def draw_health_bar(self):
		pygame.draw.rect(self.screen, self.black, (750, 190, 210, 25))
		if self.life_remaining > 0:
			pygame.draw.rect(self.screen, self.green, (750, 190, int(210 * (self.life_remaining / self.life_start)), 25))

	def calculate_value_from_key_pressed(self, key):
		speed = 450
		dx = 0
		dy = 0

		bullet_spread = 35
		bullet_extra_spread = (-10, 20, 30, 20, -10)
		self.show_hitbox = False

		if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
			speed = 120
			bullet_spread = 15
			bullet_extra_spread = (0, 8, 16, 8, 0)
			self.show_hitbox = True
		
		if key[pygame.K_LEFT] and self.rect.left > 20:
			dx = -1
			if not self.invincible:
				self.direction = "left"
		elif key[pygame.K_RIGHT] and self.rect.right < self.screen_width - 410:
			dx = 1
			if not self.invincible:
				self.direction = "right"
		else:
			self.direction = "idle"
		if key[pygame.K_UP] and self.rect.top > 0:
			dy = -1
		if key[pygame.K_DOWN] and self.rect.bottom < self.screen_height:
			dy = 1

		if dx != 0 and dy != 0:
			dx /= sqrt(2)
			dy /= sqrt(2)
		return speed, dx, dy, bullet_spread, bullet_extra_spread

	def move(self, speed, dx, dy, dt):
		self.pos.x += dx * speed * dt
		self.rect.x = round(self.pos.x)
		self.pos.y += dy * speed * dt
		self.rect.y = round(self.pos.y)
		self.mask = pygame.mask.from_surface(self.hitbox_image)

	def shoot(self, bullet_spread, bullet_extra_spread, key):
		cooldown = 0.1
		if self.stop_shooting == False:
			bullet_spread += bullet_extra_spread[self.extra_spread_pos]
			if key[pygame.K_z] and self.shoot_timer.get_elapsed_time() > cooldown:
				self.shooting_sound.play()
				bullet1 = PlayerBullet(self.rect.centerx - bullet_spread, self.rect.top, self.screen_width)
				bullet2 = PlayerBullet(self.rect.centerx, self.rect.top, self.screen_width)
				bullet3 = PlayerBullet(self.rect.centerx + bullet_spread, self.rect.top, self.screen_width)
				self.playerbullet_group.add(bullet1)
				self.playerbullet_group.add(bullet2)
				self.playerbullet_group.add(bullet3)
				self.shoot_timer.restart()
				self.extra_spread_pos += 1
				if self.extra_spread_pos >= 5:
					self.extra_spread_pos = -1

	def animate(self, dt):
		self.current_frame += dt
		if self.current_frame >= self.animation_time:
			self.current_frame -= self.animation_time
			self.current_image = (self.current_image + 1) % len(self.images[self.direction])
			self.image = self.images[self.direction][self.current_image]
			
	def finish_game(self):
		self.stop_shooting = True
		self.disable_hitbox = True
		self.pause_timer()

	def play_again(self):
		self.reset_position()
		self.invincible = False
		self.life_remaining = 3
		self.stop_shooting = False
		self.disable_hitbox = False
		self.graze = 0
		self.score = 0
		self.restart_timer()

	def update(self, dt):
		key = pygame.key.get_pressed()
		speed, dx, dy, bullet_spread, bullet_extra_spread = self.calculate_value_from_key_pressed(key)
		self.move(speed, dx, dy, dt)
		self.shoot(bullet_spread, bullet_extra_spread, key)
		self.animate(dt)
		if self.invincible:
			self.make_transparent()
			
class GrazingHitbox(pygame.sprite.Sprite):
	def __init__(self, player):
		self.player = player
		self.image = pygame.Surface((player.rect.width - 20, player.rect.height - 20), pygame.SRCALPHA)
		self.rect = self.image.get_rect(center = player.rect.center)
