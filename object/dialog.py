import pygame
from function.utility import draw_text, dialog_font
from variable.var import player, enemy, screen, white, black
from object.timer import Timer

class Dialog:
    def __init__(self, text_list):
        self.show = False
        self.text_list = text_list
        self.current_text = 0
        self.total = len(self.text_list)
        self.next_sound = pygame.mixer.Sound("asset/soundeffect/next_dialog.wav")
        self.next_sound.set_volume(0.07)
        self.started = False
        self.cooldown_timer = Timer()

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

    def draw(self):
        if self.show:
            name_text, dialog_text = self.text_list[self.current_text]
            player.draw_portrait()
            enemy.draw_portrait()
            text_box_pos = [105, 550, 405, 200]
            name_pos_y = 560
            dialog_pos_x, dialog_pos_y = 135, 620
            if name_text == "PYGAME":
                name_pos_x = 115
            else:
                name_pos_x = 415
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