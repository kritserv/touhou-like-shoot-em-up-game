import pygame
from gameclass.playerobject import Player, GrazingHitbox
from gameclass.enemyobject import Enemy
from gameclass.enemybulletobject import EnemyBullet
from gameclass.backgroundobject import BackGround
from gamefunc.utility import load_setting, load_color, draw_ui_text, clear_all_bullet, load_highscore, save_hi_score

pygame.init()

clock, fps, screen_width, screen_height, screen = load_setting()
screen_info = (screen_width, screen_height, screen)
white, grey, black, red, green = load_color()
hi_score = load_highscore()

pygame.display.set_caption("Bullet Hell")

background = BackGround(screen_info)

player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemybullet_group = pygame.sprite.Group()

player = Player(screen_info, bullet_group, black, green)
player_group.add(player)

enemy = Enemy(screen_info, enemybullet_group, black, red)
enemy_group.add(enemy)
last_enemy_shot = pygame.time.get_ticks()

bullet_count = 0
run = True
while run:
	screen.fill(black)
	draw_ui_text(screen, hi_score, player.score, player.graze, clock.get_fps(), white, grey)

	clock.tick(fps)

	background.scroll_up()

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
		
	if pygame.sprite.spritecollide(enemy, bullet_group, True, pygame.sprite.collide_mask):
	    enemy.health_remaining -= 10
	    player.score += 30

	    if enemy.health_remaining <= 0:
	        enemy.kill()
	        enemy.stop_shooting = True
	        player.stop_shooting = True
	        player.invincible = False
	        player.score += 300
	        clear_all_bullet(enemybullet_group, bullet_group)
	        save_hi_score(player.score, hi_score)

	if pygame.sprite.spritecollide(player, enemybullet_group, True, pygame.sprite.collide_mask):
	    if not player.invincible:
	        player.life_remaining -= 1
	        player.reset()

	    if player.life_remaining <= 0:
	        player.kill()
	        enemy.stop_shooting = True
	        player.stop_shooting = True
	        player.disable_hitbox = True
	        clear_all_bullet(enemybullet_group, bullet_group)

	if player.invincible:
	    if pygame.time.get_ticks() - player.last_hit_time <= 2000:
	        temp_image = player.original_image.copy()
	        temp_image.set_alpha(128)
	        player.image = temp_image
	    else:
	        player.image = player.original_image
	        player.invincible = False
	        player.image.set_alpha(255)

	grazing_hitbox = GrazingHitbox(player)
	grazing_bullets = pygame.sprite.spritecollide(grazing_hitbox, enemybullet_group, False, pygame.sprite.collide_rect)
	for enemybullet in grazing_bullets:
	    if not enemybullet.grazed:
	        player.graze += 1
	        player.score += 500
	        enemybullet.grazed = True
	            
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
		    run = False

	dt = clock.tick(fps) / 100
	player.update(dt)
	enemy.update(dt)

	bullet_group.update()
	enemybullet_group.update()

	player_group.draw(screen)
	bullet_group.draw(screen)
	enemy_group.draw(screen)
	enemybullet_group.draw(screen)

	key = pygame.key.get_pressed()
	if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
	    if not player.disable_hitbox:
	        hitbox_position = player.rect.topleft
	        screen.blit(player.hitbox_image, hitbox_position)
	pygame.display.update()

pygame.quit()
