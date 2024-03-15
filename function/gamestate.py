import pygame
from variable.var import screen, white, black, player, enemy, enemybullet_group, bullet_hell, timer, game_start_sound
from function.utility import draw_text, title_font

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
	bullet_hell.start_timer()

def pause_game():
	timer.toggle_pause()
	player.toggle_pause_timer()
	enemy.toggle_pause_timer()
	bullet_hell.toggle_pause_timer()
	for enemybullet in enemybullet_group: enemybullet.toggle_pause_timer()

def finish_game():
	player.finish_game()
	enemy.finish_game()
	timer.pause()
	bullet_hell.pause_timer()
	return False

def play_again():
	game_start_sound.play()
	player.play_again()
	enemy.play_again()
	bullet_hell.play_again()
	timer.restart()

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