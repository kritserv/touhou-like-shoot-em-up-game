import pygame
from gameclass.playerobject import Player
from gameclass.enemyobject import Enemy
from gameclass.backgroundobject import BackGround

clock = pygame.time.Clock()
fps = 60
screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))
screen_info = (screen_width, screen_height, screen)

background = BackGround(screen_info)

white = (255, 255, 255)
grey = (200, 200, 200)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

player_group, bullet_group, enemy_group, enemybullet_group = [pygame.sprite.Group() for i in range(4)]
player = Player(screen_info, bullet_group, black, green)
player_group.add(player)
enemy = Enemy(screen_info, enemybullet_group, black, red)
enemy_group.add(enemy)

bullet_count = 0