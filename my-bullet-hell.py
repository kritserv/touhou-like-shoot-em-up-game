import pygame
from gamefunc.variable import clock, fps, screen, \
	black, player_group, bullet_group, \
	enemy_group, enemybullet_group, \
	player, enemy, bullet_count, background
from gamefunc.utility import draw_ui_text, \
	load_highscore, save_hi_score, \
	check_quit_game_event, check_any_key_event, \
	show_title_screen, show_play_again, play_again, \
	finish_game, check_r_key
from gamefunc.logic import bullet_hit_enemy, bullet_hit_player, \
	make_player_transparent, is_collide, \
	player_hold_shift, show_hitbox, \
	update_graze_bullet, clear_all_bullet

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
					bullet_count = 0
					player.score += 300
					save_hi_score(player.score, hi_score)
					game_start = finish_game()

			if not enemy.stop_shooting:
				if 1 <= bullet_count < 80:
					enemy.spiral_shoot(amount = 30, focus_player = True, player = player, delay_before_focus = 200)
				elif 80 <= bullet_count < 130: 
					enemy.circular_shoot(amount = 48, focus_player = False, player = player, delay_before_focus = 0)
				elif 130 <= bullet_count < 230:
					enemy.spiral_shoot_2(amount = 120, focus_player = False, player = player, delay_before_focus = 0)
				elif 230 <= bullet_count < 240:
					enemy.circular_shoot(amount = 140, focus_player = True, player = player, delay_before_focus = 600)
				elif 240 <= bullet_count < 260:
					enemy.normal_shoot(focus_player = True, player = player, delay_before_focus = 0)
				else:
					bullet_count = 0
				bullet_count += 1

			if bullet_hit_player():
				if not player.invincible:
					player.damage_and_reset()

				if player.life_remaining <= 0:
					clear_all_bullet()
					bullet_count = 0
					game_start = finish_game()
			else:
				update_graze_bullet()
						
			for event in pygame.event.get():
				run = check_quit_game_event(event)
				quick_retry = check_r_key(event)
				if quick_retry:
					clear_all_bullet()
					bullet_count = 0
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
				if not check_any_key_event(event):
					play_again()
					game_start = True

	pygame.display.update()

pygame.quit()
