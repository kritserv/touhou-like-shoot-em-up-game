import pygame
from pygame.locals import *
from math import ceil
from gameclass.playerobject import Player, GrazingHitbox
from gameclass.enemyobject import Enemy
from gameclass.enemybulletobject import EnemyBullet

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))
screen_info = (screen_width, screen_height, screen)

pygame.display.set_caption("Bullet Hell")

white = (255, 255, 255)
grey = (200, 200, 200)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

ui_font = pygame.font.SysFont(None, 26)

def draw_text(text, font, text_col, x, y):
    image = font.render(text, True, text_col)
    screen.blit(image, (x, y))

def clear_all_bullet():
    for enemybullet in enemybullet_group:
        enemybullet.kill()
    for bullet in bullet_group:
        bullet.kill()

bg = pygame.image.load("img/background.png").convert()
bg_height = bg.get_height()

scroll = 0
tiles = ceil(screen_height / bg_height) + 1

player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemybullet_group = pygame.sprite.Group()

enemy_stop_shooting = False

player = Player(screen_info, bullet_group, black, green)
player_group.add(player)

last_enemy_shot = pygame.time.get_ticks()
enemy = Enemy(screen_info, bullet_group, black, red)
enemy_group.add(enemy)

show_player_hitbox = True
run = True
while run:
	screen.fill((0, 0, 0))
	draw_text("HISCORE", ui_font, white, 650, 50)
	draw_text("SCORE", ui_font, white, 650, 100)
	draw_text(str(player.score), ui_font, white, 750, 100)
	draw_text("PLAYER", ui_font, grey, 650, 200)
	draw_text("BOMB", ui_font, grey, 650, 250)
	draw_text("POWER", ui_font, grey, 650, 350)
	draw_text("GRAZE", ui_font, grey, 650, 400)
	draw_text(str(player.graze), ui_font, white, 750, 400)

	clock.tick(fps)

	for i in range(0, tiles):
		screen.blit(bg, (20, i * bg_height + scroll))

	scroll -= 6

	if abs(scroll) > bg_height:
		scroll = 0

	time_now = pygame.time.get_ticks()
	if time_now - last_enemy_shot > enemy.cooldown and enemy_stop_shooting == False:
		enemybullet = EnemyBullet(enemy.rect.centerx, enemy.rect.bottom)
		enemybullet_group.add(enemybullet)
		last_enemy_shot = time_now
		
	if pygame.sprite.spritecollide(enemy, bullet_group, True, pygame.sprite.collide_mask):
	    enemy.health_remaining -= 10
	    player.score += 30

	    if enemy.health_remaining <= 0:
	        enemy.kill()
	        enemy_stop_shooting = True
	        player.stop_shooting = True
	        player.score += 300
	        clear_all_bullet()

	if pygame.sprite.spritecollide(player, enemybullet_group, True, pygame.sprite.collide_mask):
	    if not player.invincible:
	        player.health_remaining -= 1
	        player.reset()

	    if player.health_remaining <= 0:
	        player.kill()
	        enemy_stop_shooting = True
	        player.stop_shooting = True
	        show_player_hitbox = False
	        clear_all_bullet()

	if player.invincible:
	    if pygame.time.get_ticks() - player.last_hit_time <= 4000:
	        temp_image = player.original_image.copy()
	        temp_image.set_alpha(128)
	        player.image = temp_image
	    else:
	        player.image = player.original_image
	        player.invincible = False

	grazing_hitbox = GrazingHitbox(player)
	grazing_bullets = pygame.sprite.spritecollide(grazing_hitbox, enemybullet_group, False, pygame.sprite.collide_rect)
	for enemybullet in grazing_bullets:
	    if not enemybullet.grazed:
	        player.graze += 1
	        player.score += 500
	        enemybullet.grazed = True
	            
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
		    run = False

	dt = clock.tick(fps) / 100
	player.update(dt)
	enemy.update(dt)

	bullet_group.update()
	enemybullet_group.update()

	player_group.draw(screen)
	bullet_group.draw(screen)
	enemy_group.draw(screen)
	enemybullet_group.draw(screen)

	key = pygame.key.get_pressed()
	if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
	    if show_player_hitbox == True:
	        hitbox_position = player.rect.topleft
	        screen.blit(player.hitbox_image, hitbox_position)
	pygame.display.update()

pygame.quit()
