import pygame
import time
import asyncio
from math import sqrt, cos, sin, atan2, pi

pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption("Pygame shoot-em-up")

clock = pygame.time.Clock()

screen_width = 1024
screen_height = 768

screen = pygame.display.set_mode((screen_width, screen_height))

'''
pygbag doesn't seems to support these screen feature, 
and also the full screen toggle. I'll have to comment it out.
screen = pygame.display.set_mode((screen_width, screen_height), 
 		pygame.RESIZABLE|pygame.SCALED)
'''

screen_info = (screen_width, screen_height, screen)

white = (255, 255, 255)
grey = (200, 200, 200)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)

game_start_sound = pygame.mixer.Sound("asset/soundeffect/start_game.ogg")
game_start_sound.set_volume(0.06)

class Timer:
	def __init__(self):
		self.start_time = 0
		self.elapsed_time = 0
		self.is_paused = True

	def start_or_resume(self):
		if self.is_paused:
			self.start_time = time.time()
			self.is_paused = False

	def pause(self):
		if not self.is_paused:
			self.elapsed_time += time.time() - self.start_time
			self.is_paused = True

	def reset(self):
		self.start_time = 0
		self.elapsed_time = 0
		self.is_paused = True

	def restart(self):
		self.reset()
		self.start_or_resume()

	def toggle_pause(self):
		if self.is_paused:
			self.start_or_resume()
		else:
			self.pause()

	def get_elapsed_time(self):
		if self.is_paused:
			return round(self.elapsed_time, 3)
		else:
			return round(self.elapsed_time + time.time() - self.start_time, 3)

timer = Timer()

class PlayerBullet(pygame.sprite.Sprite):
	def __init__(self, x, y, screen_width):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("asset/img/bullet.png").convert_alpha()
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

class Player(pygame.sprite.Sprite):
	def __init__(self, screen_info, playerbullet_group, black, green, yellow):
		pygame.sprite.Sprite.__init__(self)
		self.screen_width = screen_info[0]
		self.screen_height = screen_info[1]
		self.screen = screen_info[2]
		self.x = int(self.screen_width / 2) - 200
		self.y = self.screen_height - 100
		self.black = black
		self.green = green
		self.yellow = yellow
		self.spritesheet = {
			"idle": pygame.image.load("asset/img/player_idle.png").convert_alpha(),
			"left": pygame.image.load("asset/img/player_left.png").convert_alpha(),
			"right": pygame.image.load("asset/img/player_right.png").convert_alpha()
			}
		self.hitbox_image = pygame.image.load("asset/img/player_hitbox.png").convert_alpha()
		self.shooting_sound = pygame.mixer.Sound("asset/soundeffect/player_shoot.ogg")
		self.shooting_sound.set_volume(0.06)
		self.damaged_sound = pygame.mixer.Sound("asset/soundeffect/player_damaged.ogg")
		self.damaged_sound.set_volume(0.07)
		self.bomb_sound = pygame.mixer.Sound("asset/soundeffect/player_bomb.ogg")
		self.bomb_sound.set_volume(0.01)
		self.images = {key: [sprite.subsurface(pygame.Rect(j * 64, i * 64, 64, 64)) for i in range(1) for j in range(4)] for key, sprite in self.spritesheet.items()}
		self.current_image = 0
		self.image = self.images["idle"][self.current_image]
		self.original_image = self.image
		self.portrait = pygame.image.load("asset/img/player_portrait.png").convert_alpha()
		self.darker_portrait = self.portrait.copy()
		self.darker_portrait.fill((50, 50, 50, 255), special_flags=pygame.BLEND_RGBA_MULT)
		self.bomb_spritesheet = pygame.image.load("asset/img/snake.png").convert_alpha()
		self.bomb_images = [self.bomb_spritesheet.subsurface(pygame.Rect(j * 221, i * 768, 221, 768)) for i in range(1) for j in range(5)]
		self.bomb_image = self.bomb_images[0]
		self.current_bomb_frame = 0
		self.current_bomb_image = 0
		self.bomb_animation_time = 0.08
		self.bombing = False
		self.bomb_origin_pos = (185, 200)
		self.bomb_pos = (185, 200)
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.original_x = self.x
		self.original_y = self.y
		self.life_start = 3
		self.life_remaining = 3
		self.bomb_start = 3
		self.bomb_remaining = 3
		self.power = 1.00
		self.animation_time = 0.1
		self.current_frame = 0
		self.direction = "idle"
		self.playerbullet_group = playerbullet_group
		self.extra_spread_pos = 0
		self.stop_shooting = True
		self.disable_hitbox = False
		self.show_hitbox = False
		self.invincible = False
		self.score = 0
		self.graze = 0
		self.shoot_timer = Timer()
		self.invincible_timer = Timer()
		self.bomb_timer = Timer()

	def start_timer(self):
		self.shoot_timer.start_or_resume()
		self.invincible_timer.start_or_resume()
		self.bomb_timer.start_or_resume()

	def restart_timer(self):
		self.shoot_timer.restart()
		self.invincible_timer.restart()
		self.bomb_timer.restart()

	def pause_timer(self):
		self.shoot_timer.pause()
		self.invincible_timer.pause()
		self.bomb_timer.pause()

	def toggle_pause_timer(self):
		self.shoot_timer.toggle_pause()
		self.invincible_timer.toggle_pause()
		self.bomb_timer.toggle_pause()

	def draw_portrait(self, portrait_display):
		portrait_position = (-90, 200)
		if portrait_display:
			if portrait_display == 1:
				self.screen.blit(self.portrait, portrait_position)
			else:
				self.screen.blit(self.darker_portrait, portrait_position)

	def reset_position(self):
		self.rect.center = (self.original_x, self.original_y)
		self.pos = pygame.math.Vector2(self.rect.topleft)

	def damage_and_reset(self):
		self.damaged_sound.play()
		self.life_remaining -= 1
		if not self.life_remaining == 0:
			self.reset_position()
			self.direction = "idle"
			self.invincible = True
			self.last_hit_time = self.invincible_timer.get_elapsed_time()
			self.bomb_remaining = 3

	def draw_hitbox(self):
	    if not self.disable_hitbox:
	        hitbox_position = self.rect.topleft
	        self.screen.blit(self.hitbox_image, hitbox_position)

	def update_bomb(self, dt):
		if self.bombing:
			self.bomb_pos = self.bomb_pos[0], self.bomb_pos[1] - round(300 * dt)
			self.bomb_sound.play()
		else:
			self.bomb_pos = self.bomb_origin_pos

	def draw_bomb(self):
		if self.bombing:
			self.screen.blit(self.bomb_image, self.bomb_pos)

	def make_transparent(self):
	    if self.invincible_timer.get_elapsed_time() - self.last_hit_time <= 2:
	        temp_image = self.original_image.copy()
	        temp_image.set_alpha(128)
	        self.image = temp_image
	    else:
	        self.image = self.original_image
	        self.invincible = False
	        self.image.set_alpha(255)

	def draw_bomb_and_health_bar(self):
		pygame.draw.rect(self.screen, self.black, (750, 190, 210, 25))
		if self.life_remaining > 0:
			pygame.draw.rect(self.screen, self.green, (750, 190, int(210 * (self.life_remaining / self.life_start)), 25))
		pygame.draw.rect(self.screen, self.black, (750, 240, 210, 25))
		if self.bomb_remaining > 0:
			pygame.draw.rect(self.screen, self.yellow, (750, 240, int(210 * (self.bomb_remaining / self.bomb_start)), 25))

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

	def bomb(self, key):
		if self.stop_shooting == False and self.bomb_remaining > 0:
			if key[pygame.K_x] and self.bombing == False:
				self.bombing = True
				self.bomb_remaining -= 1
				self.last_bomb = self.bomb_timer.get_elapsed_time()

	def animate_bomb(self, dt):
		self.current_bomb_frame += dt
		if self.current_bomb_frame >= self.bomb_animation_time:
			self.current_bomb_frame -= self.bomb_animation_time
			self.current_bomb_image = (self.current_bomb_image + 1) % len(self.bomb_images)
			self.bomb_image = self.bomb_images[self.current_bomb_image]

	def do_bomb(self, dt):
		if self.bomb_timer.get_elapsed_time() - self.last_bomb <= 2.3:
			self.animate_bomb(dt)
		else:
			self.bombing = False
			self.bomb_timer.restart()
			self.bomb_pos = self.bomb_origin_pos

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
		self.bomb_remaining = 3
		self.stop_shooting = True
		self.disable_hitbox = False
		self.graze = 0
		self.score = 0
		self.bomb_pos = self.bomb_origin_pos
		self.bombing = False
		self.restart_timer()

	def update(self, dt):
		key = pygame.key.get_pressed()
		speed, dx, dy, bullet_spread, bullet_extra_spread = self.calculate_value_from_key_pressed(key)
		self.move(speed, dx, dy, dt)
		self.shoot(bullet_spread, bullet_extra_spread, key)
		self.bomb(key)
		self.animate(dt)
		if self.invincible:
			self.make_transparent()
			
class GrazingHitbox(pygame.sprite.Sprite):
	def __init__(self, player):
		self.player = player
		self.image = pygame.Surface((player.rect.width - 20, player.rect.height - 20), pygame.SRCALPHA)
		self.rect = self.image.get_rect(center = player.rect.center)

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, x, y, angle, speed, slow_speed, screen_width, screen_height, focus_player, style, slow_at_center, bounce_top):
		pygame.sprite.Sprite.__init__(self)
		self.style = style
		if self.style == 1:
			self.original_image = pygame.image.load("asset/img/enemy_bullet.png").convert_alpha()
			self.image = pygame.transform.rotate(self.original_image, -angle * 180 / pi)
		else:
			self.image = pygame.image.load("asset/img/enemy_bullet_round.png").convert_alpha()
		self.rect = self.image.get_rect(center = (x, y))
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.mask = pygame.mask.from_surface(self.image)
		self.grazed = False
		self.speed = speed
		self.slow_speed = slow_speed
		self.angle = angle
		self.slow_at_center = slow_at_center
		self.slowed = False
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.focus_player = focus_player
		self.direction_updated = False
		self.target_delay_timer = Timer()
		self.target_delay_timer.start_or_resume()
		if bounce_top:
			self.bounced = False
		else:
			self.bounced = True
		self.vx = 0
		self.vy = 0

	def toggle_pause_timer(self):
		self.target_delay_timer.toggle_pause()

	def set_target(self, target_x, target_y, delay):
		self.target_x = target_x
		self.target_y = target_y
		self.delay = delay
		self.create_time = self.target_delay_timer.get_elapsed_time()

	def focus_on_player(self):
		if self.target_delay_timer.get_elapsed_time() - self.create_time > self.delay and not self.direction_updated:
			dx = self.target_x - self.rect.centerx
			dy = self.target_y - self.rect.centery
			self.angle = atan2(dy, dx)
			if self.style == 1:
				self.image = pygame.transform.rotate(self.original_image, -self.angle * 180 / pi)
			self.vx = self.speed * cos(self.angle)
			self.vy = self.speed * sin(self.angle)
			self.direction_updated = True

	def move(self, dt):
		self.vx = self.speed * cos(self.angle)
		self.vy = self.speed * sin(self.angle)
		self.pos.y += self.vy * dt
		self.rect.y = round(self.pos.y)
		self.pos.x += self.vx * dt
		self.rect.x = round(self.pos.x)

	def bounce(self):
		self.vx = -self.vx
		self.vy = -self.vy
		self.angle = -self.angle
		if self.style == 1:
			self.image = pygame.transform.rotate(self.original_image, -self.angle * 180 / pi)

	def hit_bottom_border(self):
		return self.rect.top > self.screen_height

	def hit_top_border(self):
		return self.rect.bottom < 0

	def hit_left_border(self):
		return self.rect.left < 12

	def hit_right_border(self):
		return self.rect.right > self.screen_width - 395

	def slow_down_at_center(self):
		if self.slow_at_center:
			if self.rect.centery > self.screen_height / 2:
				self.speed = self.slow_speed
				self.slowed = True

	def update(self, dt):
		if self.hit_top_border():
			if not self.bounced:
				self.bounce()
				self.bounced = True
			else:
				self.kill()

		if self.hit_left_border() or self.hit_right_border() or self.hit_bottom_border():
			self.kill()

		if not self.slowed:
			self.slow_down_at_center()

		self.move(dt)

		if self.focus_player:
			self.focus_on_player()

class Enemy(pygame.sprite.Sprite):
	def __init__(self, screen_info, enemybullet_group, black, red):
		pygame.sprite.Sprite.__init__(self)
		self.screen_width = screen_info[0]
		self.screen_height = screen_info[1]
		self.screen = screen_info[2]
		self.x = int(self.screen_width / 2) - 200
		self.y = self.screen_height - 810
		self.black = black
		self.red = red
		self.spritesheet = {
			"idle": pygame.image.load("asset/img/enemy_idle.png").convert_alpha(),
			"left": pygame.image.load("asset/img/enemy_left.png").convert_alpha(),
			"right": pygame.image.load("asset/img/enemy_right.png").convert_alpha()
			}
		self.shooting_sound = pygame.mixer.Sound("asset/soundeffect/enemy_shoot.ogg")
		self.shooting_sound.set_volume(0.05)
		self.damaged_sound = pygame.mixer.Sound("asset/soundeffect/enemy_damaged.ogg")
		self.damaged_sound.set_volume(0.07)
		self.death_sound = pygame.mixer.Sound("asset/soundeffect/enemy_death.ogg")
		self.death_sound.set_volume(0.07)
		self.images = {key: [sprite.subsurface(pygame.Rect(j * 72, i * 88, 72, 88)) for i in range(1) for j in range(4)] for key, sprite in self.spritesheet.items()}
		self.current_image = 0
		self.image = self.images["idle"][self.current_image]
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.health_start = 500
		self.health_remaining = 1
		self.life_remaining = 2
		self.show_life = False
		self.need_healing = False
		self.is_healing = False
		self.speed = 120
		self.shoot_timer = Timer()
		self.bomb_damage_timer = Timer()
		self.bullet_delay = 0.6
		self.bullet_spiral_delay = 0.06
		self.last_bullet_time = self.shoot_timer.get_elapsed_time()
		self.last_bomb_time = self.bomb_damage_timer.get_elapsed_time()
		self.bullet_index = 0
		self.animation_time = 0.1
		self.portrait = pygame.image.load("asset/img/enemy_portrait.png").convert_alpha()
		self.darker_portrait = self.portrait.copy()
		self.darker_portrait.fill((50, 50, 50, 255), special_flags=pygame.BLEND_RGBA_MULT)
		self.current_frame = 0
		self.current_time = 0
		self.current_bomb_time = 0
		self.direction = "idle"
		self.stop_shooting = True
		self.invincible = True
		self.is_dead = False
		self.enemybullet_group = enemybullet_group

	def start_timer(self):
		self.shoot_timer.start_or_resume()
		self.bomb_damage_timer.start_or_resume()

	def restart_timer(self):
		self.shoot_timer.restart()
		self.last_bullet_time = self.shoot_timer.get_elapsed_time()
		self.bomb_damage_timer.restart()
		self.last_bomb_time = self.bomb_damage_timer.get_elapsed_time()

	def pause_timer(self):
		self.shoot_timer.pause()
		self.bomb_damage_timer.pause()

	def toggle_pause_timer(self):
		self.shoot_timer.toggle_pause()
		self.bomb_damage_timer.toggle_pause()

	def draw_portrait(self, portrait_display):
		portrait_position = (320, 200)
		if portrait_display:
			if portrait_display == 1:
				self.screen.blit(self.portrait, portrait_position)
			else:
				self.screen.blit(self.darker_portrait, portrait_position)

	def refill_health(self, dt):
		if self.health_remaining < 500:
			if not self.shoot_timer.is_paused:
				if not self.invincible:
					self.invincible = True
				if not self.show_life:
					self.show_life = True
				regen = 250 * dt
				self.health_remaining += regen
		else:
			self.invincible = False

	def respawn(self):
		self.rect.center = (self.x, self.y + 250)
		self.pos = pygame.math.Vector2(self.rect.topleft)

	def take_damage(self, value):
		self.damaged_sound.play()
		self.health_remaining -= value

	def take_1_life(self):
		self.respawn()
		self.life_remaining -= 1
		self.need_healing = True
		self.invincible = True

	def normal_shoot(self, focus_player, player, delay_before_focus, style, speed, changed_speed, change_speed_at_center, bounce_top):
		self.current_time = self.shoot_timer.get_elapsed_time()
		if self.current_time - self.last_bullet_time > self.bullet_delay and self.stop_shooting == False:
			self.shooting_sound.play()
			self.last_bullet_time = self.current_time
			bullet = EnemyBullet(self.rect.centerx, self.rect.centery, pi / 2, speed, changed_speed, self.screen_width, self.screen_height, focus_player, style, change_speed_at_center, bounce_top)
			if focus_player:
				bullet.set_target(player.rect.centerx, player.rect.centery, delay_before_focus)
			self.enemybullet_group.add(bullet)

	def circular_shoot(self, amount, focus_player, player, delay_before_focus, style, speed, changed_speed, change_speed_at_center, bounce_top):
		self.current_time = self.shoot_timer.get_elapsed_time()
		if self.current_time - self.last_bullet_time > self.bullet_delay and self.stop_shooting == False:
			self.shooting_sound.play()
			self.last_bullet_time = self.current_time
			for i in range(amount):
				angle = 2 * pi * i / amount
				bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle, speed, changed_speed, self.screen_width, self.screen_height, focus_player, style, change_speed_at_center, bounce_top)
				if focus_player:
					bullet.set_target(player.rect.centerx, player.rect.centery, delay_before_focus)
				self.enemybullet_group.add(bullet)

	def spiral_shoot(self, amount, focus_player, player, delay_before_focus, style, speed, changed_speed, change_speed_at_center, bounce_top):
		self.current_time = self.shoot_timer.get_elapsed_time()
		if self.current_time - self.last_bullet_time > self.bullet_spiral_delay:
			self.shooting_sound.play()
			self.last_bullet_time = self.current_time
			angle = 2 * pi * self.bullet_index / amount
			bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle, speed, changed_speed, self.screen_width, self.screen_height, focus_player, style, change_speed_at_center, bounce_top)
			if focus_player:
				bullet.set_target(player.rect.centerx, player.rect.centery, delay_before_focus)
			self.enemybullet_group.add(bullet)
			self.bullet_index = (self.bullet_index + 1) % amount

	def spiral_shoot_2(self, amount, focus_player, player, delay_before_focus, style, speed, changed_speed, change_speed_at_center, bounce_top):
		self.current_time = self.shoot_timer.get_elapsed_time()
		if self.current_time - self.last_bullet_time > self.bullet_spiral_delay:
			self.shooting_sound.play()
			self.last_bullet_time = self.current_time
			angle = 2 * pi * self.bullet_index / amount
			bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle, speed, changed_speed, self.screen_width, self.screen_height, focus_player, style, change_speed_at_center, bounce_top)
			if focus_player:
				bullet.set_target(player.rect.centerx, player.rect.centery, delay_before_focus)
			self.enemybullet_group.add(bullet)
			another_bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle + pi, speed, changed_speed, self.screen_width, self.screen_height, focus_player, style, change_speed_at_center, bounce_top)
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

	def take_bomb_damage(self):
		self.current_bomb_time = self.bomb_damage_timer.get_elapsed_time()
		if self.current_bomb_time - self.last_bomb_time > 0.5:
			self.take_damage(20)
			self.last_bomb_time = self.current_bomb_time

	def draw_health_bar(self):
		if self.health_remaining > 1:
			pygame.draw.rect(self.screen, self.black, (155, 20, 430, 15))
			pygame.draw.rect(self.screen, self.red, (155, 20, int(430 * (self.health_remaining / self.health_start)), 15))

	def animate(self, dt):
		self.current_frame += dt
		if self.current_frame >= self.animation_time:
			self.current_frame -= self.animation_time
			self.current_image = (self.current_image + 1) % len(self.images[self.direction])
			self.image = self.images[self.direction][self.current_image]

	def healing(self, dt):
		if self.need_healing:
			self.direction = "idle"
			self.refill_health(dt)
			self.stop_shooting = True
			self.is_healing = True

		if self.health_remaining >= self.health_start:
			self.need_healing = False
			self.invincible = False
			self.stop_shooting = False
			self.is_healing = False

	def dying(self):
		self.reset_position()
		self.death_sound.play()
		self.stop_shooting = True
		self.show_life = False

	def finish_game(self):
		self.stop_shooting = True
		self.pause_timer()

	def play_again(self):
		self.reset_position()
		self.health_remaining = 1
		self.stop_shooting = True
		self.invincible = True
		self.restart_timer()
		self.bullet_delay = 0.6
		self.bullet_spiral_delay = 0.06
		self.bullet_index = 0
		self.direction = "idle"
		self.speed = 120
		self.show_life = False
		self.life_remaining = 2
		self.need_healing = False
		self.is_healing = False
		self.is_dead = False

	def update(self, dt):
		self.animate(dt)
		self.move_mask()
		self.healing(dt)

class BulletHell:
	def __init__(self, enemy, player):
		self.enemy = enemy
		self.player = player
		self.timer = Timer()

	def start_timer(self):
		self.timer.start_or_resume()

	def restart_timer(self):
		self.timer.restart()

	def pause_timer(self):
		self.timer.pause()

	def toggle_pause_timer(self):
		self.timer.toggle_pause()

	def set_shoot_delay(self, value):
		self.enemy.bullet_delay = value
		self.enemy.bullet_spiral_delay = value * 0.1

	def pattern_0(self, dt):
		self.set_shoot_delay(0.9)
		self.enemy.circular_shoot(amount = 20, 
			focus_player = False, 
			player = self.player, 
			delay_before_focus = 0, 
			style = 1, 
			speed = 500, 
			changed_speed = 220, 
			change_speed_at_center = True, 
			bounce_top = True)
		self.enemy.move_down(dt)

	def pattern_1(self, dt):
		self.set_shoot_delay(0.2)
		self.enemy.spiral_shoot(amount = 30, 
			focus_player = True, 
			player = self.player, 
			delay_before_focus = 0.5, 
			style = 1, 
			speed = 250, 
			changed_speed = None, 
			change_speed_at_center = False, 
			bounce_top = True)
		self.enemy.move_up(dt)

	def pattern_2(self, dt):
		self.set_shoot_delay(0.05)
		self.enemy.normal_shoot(focus_player = False, 
			player = self.player, 
			delay_before_focus = 0, 
			style = 1, 
			speed = 450, 
			changed_speed = 0, 
			change_speed_at_center = False, 
			bounce_top = False)

	def pattern_3(self, dt):
		self.set_shoot_delay(0.05)
		self.enemy.circular_shoot(amount = 14, 
			focus_player = False, 
			player = self.player, 
			delay_before_focus = 0, 
			style = 1, 
			speed = 220, 
			changed_speed = 190, 
			change_speed_at_center = True, 
			bounce_top = False)

	def pattern_4(self, dt):
		self.set_shoot_delay(0.5)
		self.enemy.circular_shoot(amount = 24, 
			focus_player = False, 
			player = self.player, 
			delay_before_focus = 0, 
			style = 0, 
			speed = 320, 
			changed_speed = 190, 
			change_speed_at_center = True, 
			bounce_top = True)

	def pattern_5(self, dt):
		self.set_shoot_delay(0.2)
		self.enemy.spiral_shoot_2(amount = 90, 
			focus_player = False, 
			player = self.player, 
			delay_before_focus = 0, 
			style = 1, 
			speed = 320, 
			changed_speed = 150, 
			change_speed_at_center = True, 
			bounce_top = True)

	def pattern_6(self, dt):
		self.set_shoot_delay(0.15)
		self.enemy.spiral_shoot_2(amount = 75, 
			focus_player = True, 
			player = self.player, 
			delay_before_focus = 1.0, 
			style = 1, 
			speed = 320, 
			changed_speed = 250, 
			change_speed_at_center = True, 
			bounce_top = False)

	def pattern_7(self, dt):
		self.set_shoot_delay(0.5)
		self.enemy.circular_shoot(amount = 37, 
			focus_player = False, 
			player = self.player, 
			delay_before_focus = 0, 
			style = 0, 
			speed = 210, 
			changed_speed = 0, 
			change_speed_at_center = False, 
			bounce_top = True)

	def phase_1(self, dt, current_time):
		if 0 <= current_time < 5.0:
			self.enemy.direction = "idle"
			self.pattern_7(dt)
		elif 5.0 <= current_time < 8.0:
			self.enemy.speed = 50
			self.pattern_0(dt)
			self.enemy.move_left(dt)
			self.enemy.direction = "left"
		elif 8.0 <= current_time < 9.0:
			self.enemy.speed = 180
			self.enemy.move_right(dt)
			self.enemy.direction = "right"
		elif 9.0 <= current_time < 12.0:
			self.enemy.speed = 50
			self.pattern_1(dt)
			self.enemy.move_right(dt)
			self.enemy.direction = "right"
		elif 12.0 <= current_time < 14.2:
			self.enemy.direction = "idle"
		elif 14.2 <= current_time < 15.2:
			self.enemy.speed = 180
			self.enemy.move_left(dt)
			self.enemy.direction = "left"
		else:
			self.restart_timer()

	def phase_2(self, dt, current_time):
		if 0 <= current_time < 0.2:
			self.enemy.speed = 400
			self.enemy.move_left(dt)
			self.enemy.direction = "left"
		elif 0.2 <= current_time < 0.4:
			self.enemy.direction = "idle"
			self.pattern_3(dt)
		elif 0.4 <= current_time < 0.6:
			self.enemy.move_left(dt)
			self.enemy.direction = "left"
		elif 0.6 <= current_time < 0.8:
			self.enemy.direction = "idle"
			self.pattern_3(dt)
		elif 0.8 <= current_time < 1.0:
			self.enemy.speed = 800
			self.enemy.move_right(dt)
			self.enemy.direction = "right"
		elif 1.0 <= current_time < 1.2:
			self.enemy.speed = 400
			self.enemy.direction = "idle"
			self.pattern_3(dt)
		elif 1.2 <= current_time < 1.4:
			self.enemy.direction = "right"
			self.enemy.move_right(dt)
		elif 1.4 <= current_time < 1.6:
			self.enemy.direction = "idle"
		elif 1.6 <= current_time < 1.8:
			self.enemy.direction = "left"
			self.enemy.move_left(dt)
			self.pattern_2(dt)
		elif 1.8 <= current_time < 2.2:
			self.enemy.direction = "idle"
			self.pattern_2(dt)
		elif 2.2 <= current_time < 3.0:
			self.pattern_3(dt)
			self.enemy.direction = "right"
			self.enemy.move_right(dt)
			self.enemy.move_down(dt)
		elif 3.0 <= current_time < 4.5:
			self.enemy.direction = "idle"
		elif 4.5 <= current_time < 5.3:
			self.pattern_3(dt)
			self.enemy.direction = "left"
			self.enemy.move_left(dt)
			self.enemy.move_up(dt)
		elif 5.3 <= current_time < 6.5:
			self.enemy.direction = "idle"
		elif 6.5 <= current_time < 8.5:
			self.enemy.direction = "idle"
			self.pattern_4(dt)
		elif 8.5 <= current_time < 10.0:
			self.enemy.direction = "idle"
		elif 10.0 <= current_time < 14.0:
			self.enemy.direction = "idle"
			self.pattern_5(dt)
		elif 14.0 <= current_time < 16.0:
			self.enemy.direction = "idle"
		else:
			self.restart_timer()

	def phase_3(self, dt, current_time):
		if 0 <= current_time < 0.2:
			self.enemy.speed = 120
			self.enemy.move_right(dt)
			self.enemy.move_down(dt)
			self.enemy.direction = "right"
		elif 0.2 <= current_time < 1.0:
			self.enemy.speed = 20
			self.enemy.direction = "idle"
			self.enemy.move_up(dt)
			self.pattern_7(dt)
		elif 1.0 <= current_time < 5.0:
			self.enemy.direction = "idle"
			self.pattern_6(dt)
		elif 5.0 <= current_time < 5.2:
			self.enemy.speed = 120
			self.enemy.move_up(dt)
			self.enemy.move_left(dt)
			self.enemy.direction = "left"
		elif 5.2 <= current_time < 6.0:
			self.enemy.speed = 20
			self.enemy.move_down(dt)
			self.enemy.direction = "idle"
		elif 6.0 <= current_time < 8.0:
			self.enemy.direction = "idle"
		elif 8.0 <= current_time < 9.0:
			self.enemy.speed = 170
			self.enemy.move_left(dt)
			self.enemy.move_down(dt)
			self.enemy.direction = "left"
			self.pattern_2(dt)
		elif 9.0 <= current_time < 12.0:
			self.enemy.direction = "idle"
			self.pattern_7(dt)
		elif 12.0 <= current_time < 13.0:
			self.enemy.move_right(dt)
			self.enemy.move_up(dt)
			self.enemy.direction = "right"
			self.pattern_2(dt)
		elif 13.0 <= current_time < 15.0:
			self.enemy.direction = "idle"
		else:
			self.restart_timer()

	def play_again(self):
		self.restart_timer()

	def update(self, dt):
		if not self.enemy.stop_shooting:
			current_time = self.timer.get_elapsed_time()
			if self.enemy.life_remaining == 2:
				self.phase_1(dt, current_time)
			elif self.enemy.life_remaining == 1:
				self.phase_2(dt, current_time)
			else:
				self.phase_3(dt, current_time)

class BackGround(pygame.sprite.Sprite):
	def __init__(self, screen_info):
		pygame.sprite.Sprite.__init__(self)
		self.bg = pygame.image.load("asset/img/background.png").convert()
		self.bg_height = self.bg.get_height()
		self.screen_width = screen_info[0]
		self.screen_height = screen_info[1]
		self.screen = screen_info[2]
		self.scrolls = 0

	def scroll_up(self):
		self.screen.blit(self.bg, (20, self.scrolls))
		self.screen.blit(self.bg, (20, self.bg_height + self.scrolls))

		if abs(self.scrolls) > self.bg_height:
			self.scrolls = 0
		
	def scroll_down(self):
		self.screen.blit(self.bg, (20, -self.bg_height - self.scrolls))
		self.screen.blit(self.bg, (20, 0 - self.scrolls))

		if self.scrolls < -self.bg_height:
		 	self.scrolls = 0

	def draw(self, scrolling_up):
		if scrolling_up:
			self.scroll_up()
		else:
			self.scroll_down()

	def update(self, dt):
		self.scrolls -= 160 * dt

class Dialog:
    def __init__(self, text_list):
        self.show = False
        self.text_list = text_list
        self.current_text = 0
        self.total = len(self.text_list)
        self.next_sound = pygame.mixer.Sound("asset/soundeffect/next_dialog.ogg")
        self.next_sound.set_volume(0.07)
        self.started = False
        self.cooldown_timer = Timer()
        self.player_display = 0
        self.enemy_display = 0

    def start(self):
        if not self.started:
            self.show = True
            self.cooldown_timer.start_or_resume()
            self.started = True

    def next(self):
        if self.cooldown_timer.get_elapsed_time() >= 0.3:
            self.next_sound.play()
            self.current_text += 1
            self.cooldown_timer.restart()
        if self.current_text >= self.total:
            self.stop()

    def stop(self):
        self.show = False
        self.cooldown_timer.pause()

    def restart(self):
        self.show = False
        self.current_text = 0
        self.started = False
        self.cooldown_timer.reset()
        self.player_display = 0
        self.enemy_display = 0

    def draw(self):
        if self.show:
            name_text, dialog_text = self.text_list[self.current_text]
            if name_text == "PYGAME" and self.player_display == 0:
                self.player_display = 1
            if name_text == "ENEMY" and self.enemy_display == 0:
                self.enemy_display = 1
            if self.player_display != 0 and self.enemy_display != 0:
                if name_text == "PYGAME":
                    self.player_display = 1
                    self.enemy_display = 2
                elif name_text == "ENEMY":
                    self.player_display = 2
                    self.enemy_display = 1
            dialog_pos_x, dialog_pos_y = 135, 620
            if name_text == "PYGAME":
                name_pos_x = 115
            else:
                name_pos_x = 415
            player.draw_portrait(self.player_display)
            enemy.draw_portrait(self.enemy_display)
            text_box_pos = [105, 550, 405, 200]
            name_pos_y = 560
            pygame.draw.rect(screen, black, text_box_pos)
            draw_text(
                name_text, 
                dialog_font, 
                white, 
                name_pos_x, 
                name_pos_y, 
                screen
                )
            draw_text(
                dialog_text, 
                dialog_font, 
                white, 
                dialog_pos_x, 
                dialog_pos_y, 
                screen
                )

    def update(self):
        if self.show:
            key = pygame.key.get_pressed()
            if (key[pygame.K_z] or key[pygame.K_x] or key[pygame.K_LCTRL] or key[pygame.K_RCTRL]) \
            and self.current_text < self.total:
                self.next()

player_group, playerbullet_group, enemy_group, enemybullet_group = [pygame.sprite.Group() for i in range(4)]
player = Player(screen_info, playerbullet_group, black, green, yellow)
player_group.add(player)
enemy = Enemy(screen_info, enemybullet_group, black, red)
enemy_group.add(enemy)
bullet_hell = BulletHell(enemy, player)
background = BackGround(screen_info)

ui_font = pygame.font.SysFont(None, 26)
title_font = pygame.font.SysFont(None, 45)
dialog_font = pygame.font.SysFont(None, 32)
game_font = pygame.font.SysFont(None, 42)

def show_title_screen():
	screen.fill(white)
	draw_text("PRESS ANY KEY TO START", title_font, black, 310, 584, screen)

def show_play_again():
	pygame.draw.rect(screen, black, [105, 575, 405, 40])
	draw_text("PRESS R TO PLAY AGAIN", title_font, white, 120, 584, screen)

def show_pause_menu():
    pygame.draw.rect(screen, black, [105, 250, 405, 40])
    pygame.draw.rect(screen, black, [105, 350, 405, 40])
    #pygame.draw.rect(screen, black, [105, 450, 405, 40])
    #pygame.draw.rect(screen, black, [105, 550, 405, 40])
    draw_text("R TO RETRY", title_font, white, 225, 259, screen)
    draw_text("ESC TO UNPAUSE", title_font, white, 180, 359, screen)
    #draw_text("F OR F11 TO FULLSCREEN", title_font, white, 120, 459, screen)
    #draw_text("CTRL+Q TO QUIT", title_font, white, 180, 559, screen)

def start_game():
	game_start_sound.play()
	timer.start_or_resume()
	player.start_timer()
	enemy.start_timer()
	bullet_hell.start_timer()

def pause_game():
	timer.toggle_pause()
	player.toggle_pause_timer()
	enemy.toggle_pause_timer()
	bullet_hell.toggle_pause_timer()
	for enemybullet in enemybullet_group: enemybullet.toggle_pause_timer()

def finish_game():
	player.finish_game()
	enemy.finish_game()
	timer.pause()
	bullet_hell.pause_timer()
	return False

def play_again():
	game_start_sound.play()
	player.play_again()
	enemy.play_again()
	bullet_hell.play_again()
	timer.restart()

def save_hi_score(player_score, hi_score):
	if player_score >= hi_score:
		with open("hiscore.txt", "w") as file:
			file.write(str(player_score))
		file.close()
		
def load_highscore():
	try:
		with open("hiscore.txt", "r") as file:
			return int(file.read())
	except:
		with open("hiscore.txt", "w") as file:
			file.write("0")
		file.close()
		return 0

def draw_text(text, font, text_col, x, y, screen):
	image = font.render(text, True, text_col)
	screen.blit(image, (x, y))

def draw_ui_text(hi_score):
	if player.score >= hi_score:
		hi_score = player.score
	draw_text("HISCORE", ui_font, white, 650, 50, screen)
	draw_text(str(hi_score), ui_font, white, 750, 50, screen)
	draw_text("SCORE", ui_font, white, 650, 100, screen)
	draw_text(str(player.score), ui_font, white, 750, 100, screen)
	draw_text("PLAYER", ui_font, grey, 650, 200, screen)
	draw_text("BOMB", ui_font, grey, 650, 250, screen)
	draw_text("POWER", ui_font, grey, 650, 350, screen)
	draw_text("%s / 4.00" % str(player.power), ui_font, white, 750, 350, screen)
	draw_text("GRAZE", ui_font, grey, 650, 400, screen)
	draw_text(str(player.graze), ui_font, white, 750, 400, screen)
	draw_text("TIMER", ui_font, white, 630, 720, screen)
	draw_text(str(timer.get_elapsed_time()), ui_font, white, 690, 720, screen)
	draw_text(str(clock.get_fps() // 0.1 / 10), ui_font, white, 940, 720, screen)
	draw_text("fps", ui_font, white, 990, 720, screen)

def draw_enemy_life():
	if enemy.show_life:
		draw_text("Enemy "+str(enemy.life_remaining), title_font, white, 22, 15, screen)

def draw_every_thing(pause, hi_score, start_dialog, ending_dialog):
	screen.fill(black)
	background.draw(0)
	player.draw_bomb_and_health_bar()
	draw_ui_text(hi_score)
	enemy.draw_health_bar()
	draw_enemy_life()
	player_group.draw(screen)
	if player.show_hitbox:
		player.draw_hitbox()
	player.draw_bomb()
	playerbullet_group.draw(screen)
	enemy_group.draw(screen)
	enemybullet_group.draw(screen)
	if start_dialog.show:
		start_dialog.draw()
	if ending_dialog.show:
		ending_dialog.draw()
	if pause:
		show_pause_menu()

def update_every_thing(dt, start_dialog, ending_dialog):
	bullet_hell.update(dt)
	background.update(dt)
	player.update(dt)
	player.update_bomb(dt)
	enemy.update(dt)
	playerbullet_group.update(dt)
	enemybullet_group.update(dt)
	start_dialog.update()
	ending_dialog.update()

def is_collide(object1, object2, method):
	if method:
		return pygame.sprite.spritecollide(object1, object2, True, pygame.sprite.collide_mask)
	else:
		return pygame.sprite.spritecollide(object1, object2, False, pygame.sprite.collide_rect)

def bullet_hit_enemy():
	return is_collide(enemy, playerbullet_group, True)

def bullet_hit_player(): 
	return is_collide(player, enemybullet_group, True)

def update_graze_bullet():
	grazing_hitbox = GrazingHitbox(player)
	grazing_bullets = is_collide(grazing_hitbox, enemybullet_group, False)
	for bullet in grazing_bullets:
		if not bullet.grazed:
			player.graze += 1
			player.score += 500
			bullet.grazed = True

def clear_all_bullet():
	for bullet in enemybullet_group:
		bullet.kill()
	for bullet in playerbullet_group:
		bullet.kill()

def bomb_enemy_and_bullet(pause, dt):
	if not pause:
		player.do_bomb(dt)
		for bullet in enemybullet_group:
			bullet.kill()
		if not enemy.invincible:
			enemy.take_bomb_damage()

def enemy_enter_scene(pause, dt, dialog):
	if 2 <= timer.get_elapsed_time() <= 4 and not pause:
		enemy.move_down(dt)
		return True
	elif timer.get_elapsed_time() > 4:
		dialog.start()
		if not dialog.show:
			bullet_hell.restart_timer()
			enemy.refill_health(dt)
			if enemy.health_remaining >= 500:
				enemy.stop_shooting = False
				player.stop_shooting = False
				enemy.speed = 50
				return False
			else:
				return True
		else:
			return True
	else:
		return True

def play_ending_dialog(dialog):
	dialog.start()
	if not dialog.show:
		return True
	else:
		return False

def check_quit_game_event(event):
	if event.type == pygame.QUIT:
		return False
	# elif event.type == pygame.KEYDOWN:
	# 	if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
	# 		return False
	# 	else:
	# 		return True
	else:
		return True

def check_any_key_event(event):
	if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
		return True
	else:
		return False

def check_r_key_event(event):
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_r:
			return True
	else:
		return False

def check_esc_key_event(event):
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_ESCAPE:
			return True
	else:
		return False

'''
def check_f_and_f11_key_event(event):
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_f or event.key == pygame.K_F11:
			pygame.display.toggle_fullscreen()
'''

async def main():
	hi_score = load_highscore()
	title_screen = True
	game_start = True
	run = True
	pause = False
	enemy_intro = True
	ending_dialog_end = False
	start_dialog = Dialog(
		[["PYGAME", "Hello! Player, Nice to meet you."],
		["PYGAME", "Welcome to my game world."],
		["PYGAME", "Allow me to be your guide."],
		["ENEMY", ". . ."],
		["PYGAME", "Oh no!"],
		["PYGAME", "How did you find your way here!?"],
		["PYGAME", "Listen up, Player ..."],
		["PYGAME", "Let's face this together."],
		["ENEMY", "You'll never defeat me."]]
	)
	ending_dialog = Dialog(
		[["ENEMY", "You're quite tough."],
		["PYGAME", "Exactly!"],
		["PYGAME", "Now, depart from this place!"],
		["ENEMY", "You've won this time."],
		["ENEMY", "Alright, I'll withdraw."],
		["PYGAME", ". . ."],
		["PYGAME", "Thank you for your help, Player."],
		["PYGAME", "You've save my world."],
		["PYGAME", "There's nothing else to see here."],
		["PYGAME", "It's time to say goodbye now..."],
		["PYGAME", "Feel free to visit me again!"],
		["PYGAME", "See you."]]
	)
	prev_time = time.time()
	
	while run:
		clock.tick()
		#clock.tick(60)
		dt = time.time() - prev_time
		prev_time = time.time()
		if title_screen:
			show_title_screen()

		else:
			if game_start:

				if enemy_intro:
					enemy_intro = enemy_enter_scene(pause, dt, start_dialog)

				if bullet_hit_enemy():
					if not enemy.invincible:
						enemy.take_damage(player.power)
						player.score += 30

				if enemy.health_remaining < 0:
					if not enemy.invincible:
						clear_all_bullet()
						if enemy.life_remaining > 0:
							enemy.death_sound.play()
							enemy.take_1_life()
						else:
							if not enemy.is_dead:
								enemy.dying()
								enemy.is_dead = True
								bullet_hell.pause_timer()
								player.score += 300
								save_hi_score(player.score, hi_score)
								timer.pause()
							ending_dialog_end = play_ending_dialog(ending_dialog)

							if ending_dialog_end:
								game_start = finish_game()

				if enemy.is_healing:
					bullet_hell.restart_timer()

				if bullet_hit_player():
					if not player.invincible:
						player.damage_and_reset()

					if player.life_remaining <= 0:
						clear_all_bullet()
						game_start = finish_game()
				else:
					update_graze_bullet()

				if player.bombing:
					bomb_enemy_and_bullet(pause, dt)

				if not pause:
					update_every_thing(dt, start_dialog, ending_dialog)

				draw_every_thing(pause, hi_score, start_dialog, ending_dialog)

			else:
				show_play_again()

		for event in pygame.event.get():
			run = check_quit_game_event(event)
			#check_f_and_f11_key_event(event)
			if title_screen:
				title_screen_toggle = check_any_key_event(event)
				if title_screen_toggle:
					start_game()
					title_screen = not title_screen
			if game_start:
				toggle_pause = check_esc_key_event(event)
				if toggle_pause:
					pause_game()
					pause = not pause
				quick_retry = check_r_key_event(event)
				if quick_retry:
					if pause:
						pause = not pause
					clear_all_bullet()
					enemy_intro = True
					ending_dialog_end = False
					start_dialog.restart()
					ending_dialog.restart()
					play_again()
			else:
				retry = check_r_key_event(event)
				if retry:
					play_again()
					enemy_intro = True
					ending_dialog_end = False
					hi_score = load_highscore()
					game_start = True
					start_dialog.restart()
					ending_dialog.restart()


		pygame.display.flip()
		await asyncio.sleep(0)

	pygame.quit()

if __name__ == "__main__":
	asyncio.run(main())