import pygame
from math import ceil

class BackGround():
    def __init__(self, screen_info):
        self.bg = pygame.image.load("img/background.png").convert()
        self.bg_height = self.bg.get_height()
        self.screen_width = screen_info[0]
        self.screen_height = screen_info[1]
        self.screen = screen_info[2]
        self.scroll = 0
        self.tiles = ceil(self.screen_height / self.bg_height) + 1
        
    def scroll_up(self):
        for i in range(0, self.tiles):
            self.screen.blit(self.bg, (20, i * self.bg_height + self.scroll))
        self.scroll -= 6

        if abs(self.scroll) > self.bg_height:
            self.scroll = 0
