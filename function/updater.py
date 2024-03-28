from variable.var import bullet_hell, background, player, enemy, playerbullet_group, enemybullet_group

def update_every_thing(dt, dialog):
	bullet_hell.update(dt)
	background.update(dt)
	player.update(dt)
	player.update_bomb(dt)
	enemy.update(dt)
	playerbullet_group.update(dt)
	enemybullet_group.update(dt)
	dialog.update()