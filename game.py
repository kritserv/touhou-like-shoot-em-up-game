import pygame
import time

pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption("Bullet Hell")

from variable.var import clock, screen, \
	black, player_group, playerbullet_group, \
	enemy_group, enemybullet_group, \
	player, enemy, background, \
	pause, timer, game_start_sound
from function.utility import draw_ui_text, \
	load_highscore, save_hi_score, \
	show_title_screen, show_play_again, start_game, \
	play_again, pause_game, finish_game
from function.eventmanage import check_quit_game_event, \
    check_any_key_event, check_r_key_event, \
    check_esc_key_event, check_f_and_f11_key_event
from function.logic import bullet_hit_enemy, \
    bullet_hit_player, is_collide, update_graze_bullet, \
    clear_all_bullet

hi_score = load_highscore()
prev_time = time.time()
title_screen = True
game_start = True
run = True
while run:
	clock.tick()
	dt = time.time() - prev_time
	prev_time = time.time()

	if title_screen:
		show_title_screen()
					
		for event in pygame.event.get():
			run = check_quit_game_event(event)
			title_screen_toggle = check_any_key_event(event)
			if title_screen_toggle:
				start_game()
				title_screen = not title_screen
			check_f_and_f11_key_event(event)

	else:
		if game_start:
				
			if bullet_hit_enemy():
				enemy.damaged_sound.play()
				enemy.health_remaining -= 10
				player.score += 30

				if enemy.health_remaining < 0:
					enemy.death_sound.play()
					clear_all_bullet()
					player.score += 300
					save_hi_score(player.score, hi_score)
					game_start = finish_game()

			if not enemy.stop_shooting and not pause:
				enemy.circular_shoot(amount = 20, 
					focus_player = False, 
					player = player, 
					delay_before_focus = 0, 
					style = 0, 
					slow_at_center = True, 
					bounce_top = False)

			if bullet_hit_player():
				if not player.invincible:
					player.damaged_sound.play()
					player.damage_and_reset(timer)

				if player.life_remaining <= 0:
					clear_all_bullet()
					game_start = finish_game()
			else:
				update_graze_bullet()
						
			for event in pygame.event.get():
				run = check_quit_game_event(event)
				toggle_pause = check_esc_key_event(event)
				if toggle_pause:
					pause_game()
					pause = not pause
				quick_retry = check_r_key_event(event)
				if quick_retry:
					game_start_sound.play()
					if pause:
						pause = not pause
					clear_all_bullet()
					play_again()
				check_f_and_f11_key_event(event)
					
			if not pause:
				player.update(dt)
				enemy.update(dt)
				playerbullet_group.update(dt)
				enemybullet_group.update(dt)
				
			screen.fill(black)
			background.update(0, pause, dt)
			draw_ui_text(hi_score, player.score, player.graze)
			player.draw_health_bar()
			enemy.draw_health_bar()
			player_group.draw(screen)
			playerbullet_group.draw(screen)
			enemy_group.draw(screen)
			enemybullet_group.draw(screen)

			if player.show_hitbox:
			    player.draw_hitbox()

		else:
			show_play_again()

			for event in pygame.event.get():
				run = check_quit_game_event(event)
				retry = check_r_key_event(event)
				if retry:
					game_start_sound.play()
					play_again()
					hi_score = load_highscore()
					game_start = True
				check_f_and_f11_key_event(event)

	pygame.display.flip()

pygame.quit()
