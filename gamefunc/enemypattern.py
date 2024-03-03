from gamefunc.variable import enemy, player

def enemy_move_pattern(bullet_count):
	if 1 <= bullet_count < 40:
		enemy.move_left()
		enemy.direction = "left"
	elif 60 <= bullet_count < 100:
		enemy.move_down()
		enemy.direction = "idle"
	elif 150 <= bullet_count < 190:
		enemy.move_right()
		enemy.move_up()
		enemy.direction = "right"
	else:
		enemy.direction = "idle"

def enemy_shoot_pattern(bullet_count):
	if 1 <= bullet_count < 80:
		enemy.spiral_shoot(amount = 30, focus_player = True, player = player, delay_before_focus = 200)
	elif 80 <= bullet_count < 130: 
		enemy.circular_shoot(amount = 55, focus_player = False, player = player, delay_before_focus = 0)
	elif 130 <= bullet_count < 230:
		enemy.spiral_shoot_2(amount = 120, focus_player = False, player = player, delay_before_focus = 0)
	elif 230 <= bullet_count < 240:
		enemy.circular_shoot(amount = 140, focus_player = True, player = player, delay_before_focus = 600)
	elif 240 <= bullet_count < 260:
		enemy.normal_shoot(focus_player = True, player = player, delay_before_focus = 0)
	else:
		bullet_count = 0
	bullet_count += 1
	return bullet_count