import pygame
import time

pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption("Pygame shoot-em-up")

from variable.var import clock, player, enemy
from function.eventcheck import check_quit_game_event, \
    check_any_key_event, check_r_key_event, \
    check_esc_key_event, check_f_and_f11_key_event
from function.gamestate import load_highscore, \
	save_hi_score, show_title_screen, \
	show_play_again, start_game, \
	play_again, pause_game, finish_game
from function.logic import bullet_hit_enemy, \
    bullet_hit_player, update_graze_bullet, \
    clear_all_bullet, bomb_enemy_and_bullet, \
    enemy_enter_scene
from function.updater import update_every_thing
from function.drawer import draw_every_thing

def main():
	hi_score = load_highscore()
	title_screen = True
	game_start = True
	run = True
	pause = False
	enemy_intro = True
	prev_time = time.time()

	while run:
		clock.tick()
		dt = time.time() - prev_time
		prev_time = time.time()
		if title_screen:
			show_title_screen()

		else:
			if game_start:
				if enemy_intro:
					enemy_intro = enemy_enter_scene(pause, dt)

				if bullet_hit_enemy():
					enemy.take_damage(player.power)
					player.score += 30

				if enemy.health_remaining < 0:
					enemy.death_sound.play()
					clear_all_bullet()
					player.score += 300
					save_hi_score(player.score, hi_score)
					game_start = finish_game()

				if bullet_hit_player():
					if not player.invincible:
						player.damage_and_reset()

					if player.life_remaining <= 0:
						clear_all_bullet()
						game_start = finish_game()
				else:
					update_graze_bullet()

				if player.bombing:
					bomb_enemy_and_bullet(pause, dt)

				if not pause:
					update_every_thing(dt)

				draw_every_thing(pause, hi_score)

			else:
				show_play_again()

		for event in pygame.event.get():
			run = check_quit_game_event(event)
			check_f_and_f11_key_event(event)
			if title_screen:
				title_screen_toggle = check_any_key_event(event)
				if title_screen_toggle:
					start_game()
					title_screen = not title_screen
			if game_start:
				toggle_pause = check_esc_key_event(event)
				if toggle_pause:
					pause_game()
					pause = not pause
				quick_retry = check_r_key_event(event)
				if quick_retry:
					if pause:
						pause = not pause
					clear_all_bullet()
					enemy_intro = True
					play_again()
			else:
				retry = check_r_key_event(event)
				if retry:
					play_again()
					enemy_intro = True
					hi_score = load_highscore()
					game_start = True


		pygame.display.flip()

	pygame.quit()

if __name__ == "__main__":
	main()