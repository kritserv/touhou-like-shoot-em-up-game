from variable.var import background, player, enemy, playerbullet_group, enemybullet_group, player_group, enemy_group, screen, black
from function.utility import draw_ui_text, draw_enemy_life
from function.gamestate import show_pause_menu

def draw_every_thing(pause, hi_score, start_dialog, ending_dialog):
	screen.fill(black)
	background.draw(0)
	player.draw_bomb_and_health_bar()
	draw_ui_text(hi_score)
	enemy.draw_health_bar()
	draw_enemy_life()
	player_group.draw(screen)
	if player.show_hitbox:
		player.draw_hitbox()
	player.draw_bomb()
	playerbullet_group.draw(screen)
	enemy_group.draw(screen)
	enemybullet_group.draw(screen)
	if start_dialog.show:
		start_dialog.draw()
	if ending_dialog.show:
		ending_dialog.draw()
	if pause:
		show_pause_menu()