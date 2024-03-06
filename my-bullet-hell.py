import pygame
from gamefunc.variable import clock, fps, screen, \
	black, player_group, bullet_group, \
	enemy_group, enemybullet_group, \
	player, enemy, pattern_change_counter, background
from gamefunc.utility import draw_ui_text, \
	load_highscore, save_hi_score, \
	check_quit_game_event, check_any_key_event, \
	show_title_screen, show_play_again, play_again, \
	finish_game, check_r_key_event
from gamefunc.logic import bullet_hit_enemy, bullet_hit_player, \
	make_player_transparent, is_collide, \
	player_hold_shift, show_hitbox, \
	update_graze_bullet, clear_all_bullet
from gamefunc.enemypattern import enemy_shoot_pattern, \
	enemy_move_pattern

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
			title_screen = check_any_key_event(event)

	else:
		if game_start:
			clock.tick(fps)
			screen.fill(black)
			draw_ui_text(hi_score, player.score, player.graze)

			background.scroll_up()
				
			if bullet_hit_enemy():
				enemy.health_remaining -= 10
				player.score += 30

				if enemy.health_remaining < 0:
					clear_all_bullet()
					pattern_change_counter = 0
					player.score += 300
					save_hi_score(player.score, hi_score)
					game_start = finish_game()

			if not enemy.stop_shooting:
				pattern_change_counter = enemy_shoot_pattern(pattern_change_counter)
				enemy_move_pattern(pattern_change_counter)

			if bullet_hit_player():
				if not player.invincible:
					player.damage_and_reset()

				if player.life_remaining <= 0:
					clear_all_bullet()
					pattern_change_counter = 0
					game_start = finish_game()
			else:
				update_graze_bullet()
						
			for event in pygame.event.get():
				run = check_quit_game_event(event)
				quick_retry = check_r_key_event(event)
				if quick_retry:
					clear_all_bullet()
					pattern_change_counter = 0
					play_again()

			dt = clock.tick(fps) / 100
			player.update(dt)
			enemy.update(dt)

			bullet_group.update()
			enemybullet_group.update()

			player_group.draw(screen)
			bullet_group.draw(screen)
			enemy_group.draw(screen)
			enemybullet_group.draw(screen)

			if player.invincible:
				make_player_transparent()
				
			if player_hold_shift():
				show_hitbox(player)

		else:
			show_play_again()

			for event in pygame.event.get():
				run = check_quit_game_event(event)
				retry = check_r_key_event(event)
				if retry:
					play_again()
					hi_score = load_highscore()
					game_start = True

	pygame.display.update()

pygame.quit()
