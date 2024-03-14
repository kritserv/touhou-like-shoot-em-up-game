import pygame

def check_quit_game_event(event):
	if event.type == pygame.QUIT:
		return False
	elif event.type == pygame.KEYDOWN:
		if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
			return False
		else:
			return True
	else:
		return True

def check_any_key_event(event):
	if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
		return True
	else:
		return False

def check_r_key_event(event):
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_r:
			return True
	else:
		return False

def check_esc_key_event(event):
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_ESCAPE:
			return True
	else:
		return False

def check_f_and_f11_key_event(event):
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_f or event.key == pygame.K_F11:
			pygame.display.toggle_fullscreen()
