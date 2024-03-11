import pygame

class BackGround():
	def __init__(self, screen_info):
		self.bg = pygame.image.load("gameasset/img/background.png").convert()
		self.bg_height = self.bg.get_height()
		self.screen_width = screen_info[0]
		self.screen_height = screen_info[1]
		self.screen = screen_info[2]
		self.scrolls = 0

	def scroll_up(self):
		self.screen.blit(self.bg, (20, self.scrolls))
		self.screen.blit(self.bg, (20, self.bg_height + self.scrolls))

		if abs(self.scrolls) > self.bg_height:
			self.scrolls = 0
		
	def scroll_down(self):
		self.screen.blit(self.bg, (20, -self.bg_height - self.scrolls))
		self.screen.blit(self.bg, (20, 0 - self.scrolls))

		if self.scrolls < -self.bg_height:
		 	self.scrolls = 0

	def update(self, up_0_or_down_1, pause, dt):
		if up_0_or_down_1:
			self.scroll_down()
		else:
			self.scroll_up()

		if not pause:
			self.scrolls -= 160 * dt