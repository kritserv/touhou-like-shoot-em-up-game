import pygame
import time

pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption("Bullet Hell")

from variable.var import clock, screen, \
	black, player_group, playerbullet_group, \
	enemy_group, enemybullet_group, \
	player, enemy, background, bullet_hell
from function.utility import draw_ui_text
from function.eventcheck import check_quit_game_event, \
    check_any_key_event, check_r_key_event, \
    check_esc_key_event, check_f_and_f11_key_event
from function.gamestate import load_highscore, \
	save_hi_score, show_title_screen, \
	show_play_again, show_pause_menu, \
	start_game, play_again, pause_game, \
	finish_game
from function.logic import bullet_hit_enemy, \
    bullet_hit_player, update_graze_bullet, \
    clear_all_bullet, bomb_enemy_and_bullet

hi_score = load_highscore()
title_screen = True
game_start = True
run = True
pause = False
prev_time = time.time()

while run:
	clock.tick()
	dt = time.time() - prev_time
	prev_time = time.time()
	if title_screen:
		show_title_screen()

	else:
		if game_start:
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
				bullet_hell.update(dt)
				background.update(dt)
				player.update(dt)
				player.update_bomb(dt)
				enemy.update(dt)
				playerbullet_group.update(dt)
				enemybullet_group.update(dt)
				
			screen.fill(black)
			background.draw(0)
			player.draw_bomb_and_health_bar()
			draw_ui_text(hi_score)
			enemy.draw_health_bar()
			player_group.draw(screen)
			if player.show_hitbox: player.draw_hitbox()
			player.draw_bomb()
			playerbullet_group.draw(screen)
			enemy_group.draw(screen)
			enemybullet_group.draw(screen)
			if pause: show_pause_menu()

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
				play_again()
		else:
			retry = check_r_key_event(event)
			if retry:
				play_again()
				hi_score = load_highscore()
				game_start = True


	pygame.display.flip()

pygame.quit()
