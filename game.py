import pygame
from gamevariable.var import clock, fps, screen, \
	black, player_group, bullet_group, \
	enemy_group, enemybullet_group, \
	player, enemy, pattern_change_counter, background, \
	pause, game_start_sound
from gamefunc.utility import draw_ui_text, \
	load_highscore, save_hi_score, \
	check_quit_game_event, check_any_key_event, \
	show_title_screen, show_play_again, play_again, \
	finish_game, check_r_key_event, check_esc_key_event
from gamefunc.logic import bullet_hit_enemy, bullet_hit_player, \
    is_collide, update_graze_bullet, \
    clear_all_bullet
from gamefunc.enemypattern import enemy_shoot_pattern, \
	enemy_move_pattern

pygame.mixer.pre_init(44100, -8, 2, 512)
pygame.mixer.init()
pygame.init()

hi_score = load_highscore()
pygame.display.set_caption("Bullet Hell")

title_screen = True
game_start = True
run = True
while run:
	if title_screen:
		show_title_screen()
					
		for event in pygame.event.get():
			run = check_quit_game_event(event)
			title_screen_toggle = check_any_key_event(event)
			if title_screen_toggle:
				game_start_sound.play()
				title_screen = not title_screen

	else:
		if game_start:
			clock.tick(fps)
			screen.fill(black)
			draw_ui_text(hi_score, player.score, player.graze)

			background.scroll_up(pause)
				
			if bullet_hit_enemy():
				enemy.damaged_sound.play()
				enemy.health_remaining -= 10
				player.score += 30

				if enemy.health_remaining < 0:
					enemy.death_sound.play()
					clear_all_bullet()
					pattern_change_counter = 0
					player.score += 300
					save_hi_score(player.score, hi_score)
					game_start = finish_game()

			if not enemy.stop_shooting and not pause:
				pattern_change_counter = enemy_shoot_pattern(pattern_change_counter)
				enemy_move_pattern(pattern_change_counter)

			if bullet_hit_player():
				if not player.invincible:
					player.damaged_sound.play()
					player.damage_and_reset()

				if player.life_remaining <= 0:
					clear_all_bullet()
					pattern_change_counter = 0
					game_start = finish_game()
			else:
				update_graze_bullet()
						
			for event in pygame.event.get():
				run = check_quit_game_event(event)
				toggle_pause = check_esc_key_event(event)
				if toggle_pause:
					pause = not pause
				quick_retry = check_r_key_event(event)
				if quick_retry:
					game_start_sound.play()
					if pause:
						pause = not pause
					clear_all_bullet()
					pattern_change_counter = 0
					play_again()
					
			dt = clock.tick(fps) / 10
			if not pause:
				player.update(dt)
				enemy.update(dt)
				bullet_group.update()
				enemybullet_group.update()
			
			player_group.draw(screen)
			bullet_group.draw(screen)
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

	pygame.display.update()

pygame.quit()
