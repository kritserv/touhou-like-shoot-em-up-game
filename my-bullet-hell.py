import pygame
from gamefunc.variable import clock, fps, screen, \
	black, player_group, bullet_group, \
	enemy_group, enemybullet_group, \
	player, enemy, bullet_count, background
from gamefunc.utility import draw_text, draw_ui_text, \
	load_highscore, save_hi_score, \
	check_quit_game_event, check_any_key_event, \
	show_title_screen
from gamefunc.logic import bullet_hit_enemy, bullet_hit_player, \
	make_player_transparent, is_collide, \
	player_hold_shift, show_hitbox, \
	update_graze_bullet, clear_all_bullet

pygame.init()
hi_score = load_highscore()
pygame.display.set_caption("Bullet Hell")

title_screen = True
run = True
while run:
	if title_screen:
		show_title_screen()
					
		for event in pygame.event.get():
			run = check_quit_game_event(event)
			title_screen = check_any_key_event(event)

	else:
		clock.tick(fps)
		screen.fill(black)
		draw_ui_text(hi_score, player.score, player.graze)
		background.scroll_up()
			
		if bullet_hit_enemy():
			enemy.health_remaining -= 10
			player.score += 30

			if enemy.health_remaining <= 0:
				enemy.kill()
				enemy.stop_shooting = True
				player.stop_shooting = True
				player.invincible = False
				player.score += 300
				clear_all_bullet()
				save_hi_score(player.score, hi_score)

		if not enemy.stop_shooting:
			if 0 <= bullet_count < 80:
				enemy.spiral_shoot()
			elif 80 <= bullet_count < 130:
				enemy.normal_shoot()
			elif 130 <= bullet_count < 230: 
				enemy.circular_shoot()
			else:
				bullet_count = 0
			bullet_count += 1

		if bullet_hit_player():
			if not player.invincible:
				player.damage_and_reset()

			if player.life_remaining <= 0:
				player.kill()
				enemy.stop_shooting = True
				player.stop_shooting = True
				player.disable_hitbox = True
				clear_all_bullet()
		else:
			update_graze_bullet()
					
		for event in pygame.event.get():
			run = check_quit_game_event(event)

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

	pygame.display.update()

pygame.quit()
