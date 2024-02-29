import pygame
from gameclass.playerobject import GrazingHitbox
from gamefunc.variable import screen, screen_info, white, grey, black, red, green, player, enemy, bullet_group, enemybullet_group

def is_collide(object1, object2, method):
	if method:
		return pygame.sprite.spritecollide(object1, object2, True, pygame.sprite.collide_mask)
	else:
		return pygame.sprite.spritecollide(object1, object2, False, pygame.sprite.collide_rect)

def bullet_hit_enemy(): 
	return is_collide(enemy, bullet_group, True)

def bullet_hit_player(): 
	return is_collide(player, enemybullet_group, True)

def player_hold_shift():
	key = pygame.key.get_pressed()
	return key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]

def show_hitbox(player):
	if not player.disable_hitbox:
		hitbox_position = player.rect.topleft
		screen.blit(player.hitbox_image, hitbox_position)

def make_player_transparent():
	if pygame.time.get_ticks() - player.last_hit_time <= 2000:
		temp_image = player.original_image.copy()
		temp_image.set_alpha(128)
		player.image = temp_image
	else:
		player.image = player.original_image
		player.invincible = False
		player.image.set_alpha(255)

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