import pygame
from variable.var import screen, white, black
from function.utility import draw_text, dialog_font

class Dialog:
    def __init__(self):
        self.show = False
        self.text_list = [["PYGAME", "Hello, This is dialog 1."], ["ENEMY", "Hello, This is dialog 2."]]
        self.current_text = 0
        self.total = len(self.text_list)

    def start(self):
        self.show = True

    def next(self):
        self.current_text += 1

    def stop(self):
        self.show = False
        self.current_text = 0

    def draw(self):
        if self.show and self.current_text < self.total:
            pygame.draw.rect(screen, black, [105, 550, 405, 200])
            draw_text(self.text_list[self.current_text][0], dialog_font, white, 115, 560, screen)
            draw_text(self.text_list[self.current_text][1], dialog_font, white, 135, 620, screen)
