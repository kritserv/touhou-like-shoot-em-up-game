import pygame
from pygame.locals import *
from math import ceil

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1024

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bullet Hell")

bg = pygame.image.load("img/background.png").convert()
bg_height = bg.get_height()

scroll = 0
tiles = ceil(screen_height / bg_height) + 1
print(tiles)

run = True
while run:

	clock.tick(fps)

	for i in range(0, tiles):
		screen.blit(bg, (0, i * bg_height + scroll))

	scroll -= 6

	if abs(scroll) > bg_height:
		scroll = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	pygame.display.update()

pygame.quit()