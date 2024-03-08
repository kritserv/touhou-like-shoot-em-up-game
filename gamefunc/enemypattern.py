from gamevariable.var import enemy, player

def enemy_move_pattern(pattern_change_counter):
	if 1 <= pattern_change_counter < 40:
		enemy.move_left()
		enemy.direction = "left"
	elif 60 <= pattern_change_counter < 100:
		enemy.move_down()
		enemy.direction = "idle"
	elif 150 <= pattern_change_counter < 190:
		enemy.move_right()
		enemy.move_up()
		enemy.direction = "right"
	else:
		enemy.direction = "idle"

def enemy_shoot_pattern(pattern_change_counter):
	if 1 <= pattern_change_counter < 80:
		enemy.spiral_shoot(amount = 30, focus_player = True, player = player, delay_before_focus = 200, style = 1)
	elif 80 <= pattern_change_counter < 130: 
		enemy.circular_shoot(amount = 55, focus_player = False, player = player, delay_before_focus = 0, style = 0)
	elif 130 <= pattern_change_counter < 230:
		enemy.spiral_shoot_2(amount = 120, focus_player = False, player = player, delay_before_focus = 0, style = 0)
	elif 230 <= pattern_change_counter < 240:
		enemy.circular_shoot(amount = 140, focus_player = True, player = player, delay_before_focus = 600, style = 1)
	elif 240 <= pattern_change_counter < 260:
		enemy.normal_shoot(focus_player = True, player = player, delay_before_focus = 0, style = 1)
	else:
		pattern_change_counter = 0
	pattern_change_counter += 1
	return pattern_change_counter