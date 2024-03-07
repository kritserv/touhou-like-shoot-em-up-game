import pygame
from gameclass.playerobject import GrazingHitbox
from gamefunc.variable import white, grey, black, red, green, player, enemy, bullet_group, enemybullet_group

def is_collide(object1, object2, method):
	if method:
		return pygame.sprite.spritecollide(object1, object2, True, pygame.sprite.collide_mask)
	else:
		return pygame.sprite.spritecollide(object1, object2, False, pygame.sprite.collide_rect)

def bullet_hit_enemy(): 
	return is_collide(enemy, bullet_group, True)

def bullet_hit_player(): 
	return is_collide(player, enemybullet_group, True)

def update_graze_bullet():
	grazing_hitbox = GrazingHitbox(player)
	grazing_bullets = is_collide(grazing_hitbox, enemybullet_group, False)
	for enemybullet in grazing_bullets:
		if not enemybullet.grazed:
			player.graze += 1
			player.score += 500
			enemybullet.grazed = True

def clear_all_bullet():
	for enemybullet in enemybullet_group:
		enemybullet.kill()
	for bullet in bullet_group:
		bullet.kill()
