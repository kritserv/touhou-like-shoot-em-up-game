import pygame
from object.player import GrazingHitbox
from variable.var import white, grey, black, red, green, player, enemy, playerbullet_group, enemybullet_group

def is_collide(object1, object2, method):
	if method:
		return pygame.sprite.spritecollide(object1, object2, True, pygame.sprite.collide_mask)
	else:
		return pygame.sprite.spritecollide(object1, object2, False, pygame.sprite.collide_rect)

def bullet_hit_enemy():
	return is_collide(enemy, playerbullet_group, True)

def bullet_hit_player(): 
	return is_collide(player, enemybullet_group, True)

def update_graze_bullet():
	grazing_hitbox = GrazingHitbox(player)
	grazing_bullets = is_collide(grazing_hitbox, enemybullet_group, False)
	for bullet in grazing_bullets:
		if not bullet.grazed:
			player.graze += 1
			player.score += 500
			bullet.grazed = True

def clear_all_bullet():
	for bullet in enemybullet_group:
		bullet.kill()
	for bullet in playerbullet_group:
		bullet.kill()

def bomb_enemy_and_bullet(pause, dt):
	if not pause:
		player.do_bomb(dt)
		for bullet in enemybullet_group:
			bullet.kill()
		enemy.take_bomb_damage()