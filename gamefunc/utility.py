import pygame
from gamefunc.variable import clock, screen, white, grey, black, player, enemy

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
	ui_font = pygame.font.SysFont(None, 26)
	draw_text("HISCORE", ui_font, white, 650, 50, screen)
	draw_text(str(hi_score), ui_font, white, 750, 50, screen)
	draw_text("SCORE", ui_font, white, 650, 100, screen)
	draw_text(str(player_score), ui_font, white, 750, 100, screen)
	draw_text("PLAYER", ui_font, grey, 650, 200, screen)
	draw_text("BOMB", ui_font, grey, 650, 250, screen)
	draw_text("POWER", ui_font, grey, 650, 350, screen)
	draw_text("GRAZE", ui_font, grey, 650, 400, screen)
	draw_text(str(player_graze), ui_font, white, 750, 400, screen)
	draw_text(str(clock.get_fps() // 0.1 / 10), ui_font, white, 950, 720, screen)
	draw_text("fps", ui_font, white, 990, 720, screen)

def show_title_screen():
	screen.fill(white)
	title_font = pygame.font.SysFont(None, 45)
	draw_text("PRESS ANY KEY TO START", title_font, black, 310, 584, screen)

def show_play_again():
	pygame.draw.rect(screen, (0, 0, 0), [105, 575, 405, 40])
	title_font = pygame.font.SysFont(None, 45)
	draw_text("PRESS R TO PLAY AGAIN", title_font, white, 120, 584, screen)

def finish_game():
	enemy.stop_shooting = True
	player.stop_shooting = True
	player.disable_hitbox = True
	return False

def play_again():
	player.reset_position()
	enemy.reset_position()
	player.invincible = False
	player.life_remaining = 3
	enemy.health_remaining = 500
	enemy.stop_shooting = False
	player.stop_shooting = False
	player.disable_hitbox = False
	player.graze = 0
	player.score = 0

def check_quit_game_event(event):
	if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_q):
		return False
	else:
		return True

def check_any_key_event(event):
	if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
		return False
	else:
		return True

def check_r_key_event(event):
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_r:
			return True
	else:
		return False
