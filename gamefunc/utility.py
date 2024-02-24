import pygame

def load_setting():
    clock = pygame.time.Clock()
    fps = 60
    screen_width = 1024
    screen_height = 768
    screen = pygame.display.set_mode((screen_width, screen_height))
    return clock, fps, screen_width, screen_height, screen
    
def load_color():
    white = (255, 255, 255)
    grey = (200, 200, 200)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    return white, grey, black, red, green

def draw_text(text, font, text_col, x, y, screen):
    image = font.render(text, True, text_col)
    screen.blit(image, (x, y))

def draw_ui_text(screen, player_score, player_graze, white, grey):
    ui_font = pygame.font.SysFont(None, 26)
    draw_text("HISCORE", ui_font, white, 650, 50, screen)
    draw_text("SCORE", ui_font, white, 650, 100, screen)
    draw_text(str(player_score), ui_font, white, 750, 100, screen)
    draw_text("PLAYER", ui_font, grey, 650, 200, screen)
    draw_text("BOMB", ui_font, grey, 650, 250, screen)
    draw_text("POWER", ui_font, grey, 650, 350, screen)
    draw_text("GRAZE", ui_font, grey, 650, 400, screen)
    draw_text(str(player_graze), ui_font, white, 750, 400, screen)

def clear_all_bullet(enemybullet_group, bullet_group):
    for enemybullet in enemybullet_group:
        enemybullet.kill()
    for bullet in bullet_group:
        bullet.kill()
