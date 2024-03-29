import pygame
import time

pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption("Pygame shoot-em-up")

from variable.var import clock, player, enemy, \
	bullet_hell, timer
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
    enemy_enter_scene, play_ending_dialog
from function.updater import update_every_thing
from function.drawer import draw_every_thing
from object.dialog import Dialog

def main():
	hi_score = load_highscore()
	title_screen = True
	game_start = True
	run = True
	pause = False
	enemy_intro = True
	ending_dialog_end = False
	start_dialog = Dialog(
		[["PYGAME", "Hello! Player, Nice to meet you."],
		["PYGAME", "Welcome to my game world."],
		["PYGAME", "Allow me to be your guide."],
		["ENEMY", ". . ."],
		["PYGAME", "Oh no!"],
		["PYGAME", "How did you find your way here!?"],
		["PYGAME", "Listen up, Player ..."],
		["PYGAME", "Let's face this together."],
		["ENEMY", "You'll never defeat me."]]
	)
	ending_dialog = Dialog(
		[["ENEMY", "You're quite tough."],
		["PYGAME", "Exactly!"],
		["PYGAME", "Now, depart from this place!"],
		["ENEMY", "You've won this time."],
		["ENEMY", "Alright, I'll withdraw."],
		["PYGAME", ". . ."],
		["PYGAME", "Thank you for your help, Player."],
		["PYGAME", "You've save my world."],
		["PYGAME", "There's nothing else to see here."],
		["PYGAME", "It's time to say goodbye now..."],
		["PYGAME", "Feel free to visit me again!"],
		["PYGAME", "See you."]]
	)
	prev_time = time.time()
	
	while run:
		clock.tick()
		#clock.tick(60)
		dt = time.time() - prev_time
		prev_time = time.time()
		if title_screen:
			show_title_screen()

		else:
			if game_start:

				if enemy_intro:
					enemy_intro = enemy_enter_scene(pause, dt, start_dialog)

				if bullet_hit_enemy():
					if not enemy.invincible:
						enemy.take_damage(player.power)
						player.score += 30

				if enemy.health_remaining < 0:
					if not enemy.invincible:
						clear_all_bullet()
						if enemy.life_remaining > 0:
							enemy.death_sound.play()
							enemy.take_1_life()
						else:
							if not enemy.is_dead:
								enemy.dying()
								enemy.is_dead = True
								bullet_hell.pause_timer()
								player.score += 300
								save_hi_score(player.score, hi_score)
								timer.pause()
							ending_dialog_end = play_ending_dialog(ending_dialog)

							if ending_dialog_end:
								game_start = finish_game()

				if enemy.is_healing:
					bullet_hell.restart_timer()

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
					update_every_thing(dt, start_dialog, ending_dialog)

				draw_every_thing(pause, hi_score, start_dialog, ending_dialog)

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
					ending_dialog_end = False
					start_dialog.restart()
					ending_dialog.restart()
					play_again()
			else:
				retry = check_r_key_event(event)
				if retry:
					play_again()
					enemy_intro = True
					ending_dialog_end = False
					hi_score = load_highscore()
					game_start = True
					start_dialog.restart()
					ending_dialog.restart()


		pygame.display.flip()

	pygame.quit()

if __name__ == "__main__":
	main()