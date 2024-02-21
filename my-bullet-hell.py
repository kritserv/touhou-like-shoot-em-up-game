import pygame
from pygame.locals import *
from math import ceil
from playerobject import Player

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

player = Player(int(screen_width / 2) - 200, screen_height - 100, 7, bullet_group)
player_group.add(player)


run = True
while run:

	clock.tick(fps)

	for i in range(0, tiles):
		screen.blit(bg, (20, i * bg_height + scroll))

	scroll -= 6

	if abs(scroll) > bg_height:
		scroll = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	dt = clock.tick(fps) / 100
	player.update(dt)

	bullet_group.update()

	player_group.draw(screen)
	bullet_group.draw(screen)
	pygame.display.update()

pygame.quit()