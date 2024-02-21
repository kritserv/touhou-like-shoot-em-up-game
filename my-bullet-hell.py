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

player_hp = 7
player = Player(int(screen_width / 2) - 200, screen_height - 100, player_hp, bullet_group)
player_group.add(player)

enemy_hp = 500
enemy_cooldown = 500
last_enemy_shot = pygame.time.get_ticks()
enemy = Enemy(int(screen_width / 2) - 200, screen_height - 600, 500, bullet_group)
enemy_group.add(enemy)

run = True
while run:

	clock.tick(fps)

	for i in range(0, tiles):
		screen.blit(bg, (20, i * bg_height + scroll))

	scroll -= 6

	if abs(scroll) > bg_height:
		scroll = 0

	time_now = pygame.time.get_ticks()
	if time_now - last_enemy_shot > enemy_cooldown:
		enemybullet = EnemyBullet(enemy.rect.centerx, enemy.rect.bottom)
		enemybullet_group.add(enemybullet)
		last_enemy_shot = time_now

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
	pygame.display.update()

pygame.quit()