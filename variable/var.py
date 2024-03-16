import pygame
from object.player import Player
from object.enemy import Enemy
from object.background import BackGround
from object.timer import Timer
from object.bullethell import BulletHell

clock = pygame.time.Clock()

screen_width = 1024
screen_height = 768

screen = pygame.display.set_mode((screen_width, screen_height), 
		pygame.RESIZABLE|pygame.SCALED)

screen_info = (screen_width, screen_height, screen)

background = BackGround(screen_info)

white = (255, 255, 255)
grey = (200, 200, 200)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)

player_group, playerbullet_group, enemy_group, enemybullet_group = [pygame.sprite.Group() for i in range(4)]
player = Player(screen_info, playerbullet_group, black, green, yellow)
player_group.add(player)
enemy = Enemy(screen_info, enemybullet_group, black, red)
enemy_group.add(enemy)

bullet_hell = BulletHell(enemy, player)

game_start_sound = pygame.mixer.Sound("asset/soundeffect/start_game.wav")
game_start_sound.set_volume(0.06)

timer = Timer()