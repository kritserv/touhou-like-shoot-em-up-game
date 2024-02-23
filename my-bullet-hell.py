import pygame
from pygame.locals import *
from math import ceil
from gameclass.playerobject import Player
from gameclass.enemyobject import Enemy
from gameclass.enemybulletobject import EnemyBullet

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1024
screen_height = 768

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bullet Hell")

bg = pygame.image.load("img/background.png").convert()
bg_height = bg.get_height()

scroll = 0
tiles = ceil(screen_height / bg_height) + 1

player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemybullet_group = pygame.sprite.Group()

player_stop_shooting = False
enemy_stop_shooting = False

player_hp = 70
player = Player(int(screen_width / 2) - 200, screen_height - 100, player_hp, bullet_group, player_stop_shooting)
player_group.add(player)

enemy_hp = 500
enemy_cooldown = 500
last_enemy_shot = pygame.time.get_ticks()
enemy = Enemy(int(screen_width / 2) - 200, screen_height - 600, 500, bullet_group)
enemy_group.add(enemy)

show_player_hitbox = True
run = True
while run:

	clock.tick(fps)

	for i in range(0, tiles):
		screen.blit(bg, (20, i * bg_height + scroll))

	scroll -= 6

	if abs(scroll) > bg_height:
		scroll = 0

	time_now = pygame.time.get_ticks()
	if time_now - last_enemy_shot > enemy_cooldown and enemy_stop_shooting == False:
		enemybullet = EnemyBullet(enemy.rect.centerx, enemy.rect.bottom)
		enemybullet_group.add(enemybullet)
		last_enemy_shot = time_now
		
	if pygame.sprite.spritecollide(enemy, bullet_group, True, pygame.sprite.collide_mask):
	    enemy.health_remaining -= 10

	    if enemy.health_remaining <= 0:
	        enemy.kill()
	        enemy_stop_shooting = True
	        player.stop_shooting = True
	        for enemybullet in enemybullet_group:
	            enemybullet.kill()
	        for bullet in bullet_group:
	            bullet.kill()
	            
	if pygame.sprite.spritecollide(player, enemybullet_group, True, pygame.sprite.collide_mask):
	    player.health_remaining -= 10

	    if player.health_remaining <= 0:
	        player.kill()
	        enemy_stop_shooting = True
	        player.stop_shooting = True
	        show_player_hitbox = False
	        for enemybullet in enemybullet_group:
	            enemybullet.kill()
	        for bullet in bullet_group:
	            bullet.kill()

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
