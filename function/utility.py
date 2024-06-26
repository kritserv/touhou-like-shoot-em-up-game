import pygame
from variable.var import clock, screen, white, grey, player, enemy, timer

ui_font = pygame.font.SysFont(None, 26)
title_font = pygame.font.SysFont(None, 45)
dialog_font = pygame.font.SysFont(None, 32)
game_font = pygame.font.SysFont(None, 42)

def draw_text(text, font, text_col, x, y, screen):
	image = font.render(text, True, text_col)
	screen.blit(image, (x, y))

def draw_ui_text(hi_score):
	if player.score >= hi_score:
		hi_score = player.score
	draw_text("HISCORE", ui_font, white, 650, 50, screen)
	draw_text(str(hi_score), ui_font, white, 750, 50, screen)
	draw_text("SCORE", ui_font, white, 650, 100, screen)
	draw_text(str(player.score), ui_font, white, 750, 100, screen)
	draw_text("PLAYER", ui_font, grey, 650, 200, screen)
	draw_text("BOMB", ui_font, grey, 650, 250, screen)
	draw_text("POWER", ui_font, grey, 650, 350, screen)
	draw_text("%s / 4.00" % str(player.power), ui_font, white, 750, 350, screen)
	draw_text("GRAZE", ui_font, grey, 650, 400, screen)
	draw_text(str(player.graze), ui_font, white, 750, 400, screen)
	draw_text("TIMER", ui_font, white, 630, 720, screen)
	draw_text(str(timer.get_elapsed_time()), ui_font, white, 690, 720, screen)
	draw_text(str(clock.get_fps() // 0.1 / 10), ui_font, white, 940, 720, screen)
	draw_text("fps", ui_font, white, 990, 720, screen)

def draw_enemy_life():
	if enemy.show_life:
		draw_text("Enemy "+str(enemy.life_remaining), title_font, white, 22, 15, screen)
