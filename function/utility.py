import pygame
import time
from variable.var import clock, screen, white, grey, black, player, enemy, enemybullet_group, timer, game_start_sound

ui_font = pygame.font.SysFont(None, 26)
title_font = pygame.font.SysFont(None, 45)

def save_hi_score(player_score, hi_score):
	if player_score >= hi_score:
		with open(".hiscore", "w") as file:
			file.write(str(player_score))
		file.close()
		
def load_highscore():
	try:
		with open(".hiscore", "r") as file:
			return int(file.read())
	except:
		with open(".hiscore", "w") as file:
			file.write("0")
		file.close()
		return 0

def draw_text(text, font, text_col, x, y, screen):
	image = font.render(text, True, text_col)
	screen.blit(image, (x, y))

def draw_ui_text(hi_score, player_score, player_graze):
	if player_score >= hi_score:
		hi_score = player_score
	draw_text("HISCORE", ui_font, white, 650, 50, screen)
	draw_text(str(hi_score), ui_font, white, 750, 50, screen)
	draw_text("SCORE", ui_font, white, 650, 100, screen)
	draw_text(str(player_score), ui_font, white, 750, 100, screen)
	draw_text("PLAYER", ui_font, grey, 650, 200, screen)
	draw_text("BOMB", ui_font, grey, 650, 250, screen)
	draw_text("POWER", ui_font, grey, 650, 350, screen)
	draw_text("GRAZE", ui_font, grey, 650, 400, screen)
	draw_text(str(player_graze), ui_font, white, 750, 400, screen)
	draw_text("TIMER", ui_font, white, 630, 720, screen)
	draw_text(str(timer.get_elapsed_time()), ui_font, white, 690, 720, screen)
	draw_text(str(clock.get_fps() // 0.1 / 10), ui_font, white, 940, 720, screen)
	draw_text("fps", ui_font, white, 990, 720, screen)

def show_title_screen():
	screen.fill(white)
	draw_text("PRESS ANY KEY TO START", title_font, black, 310, 584, screen)

def show_play_again():
	pygame.draw.rect(screen, (0, 0, 0), [105, 575, 405, 40])
	draw_text("PRESS R TO PLAY AGAIN", title_font, white, 120, 584, screen)

def start_game():
	game_start_sound.play()
	timer.start()
	player.start_timer()
	enemy.start_timer()

def pause_game():
	timer.toggle_pause()
	player.toggle_pause_timer()
	enemy.toggle_pause_timer()
	for enemybullet in enemybullet_group: enemybullet.toggle_pause_timer()

def finish_game():
	player.finish_game()
	enemy.finish_game()
	timer.pause()
	return False

def play_again():
	player.play_again()
	enemy.play_again()
	timer.restart()
