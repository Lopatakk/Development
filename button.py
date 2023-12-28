import pygame

class Button():
	def __init__(self, x_button, y_button, image_path, scale_w, scale_h, text_size, text, screen_in_button):
		width_screen = screen_in_button.get_width()
		#	BUTTON
		image = pygame.image.load(image_path).convert_alpha()	# load button images with transparency
		self.image = pygame.transform.scale(image, (int(width_screen * scale_w), int(width_screen * scale_h)))	# transforming image
		self.rect = self.image.get_rect()	# creates a rectangular frame around the object's image
		self.rect.topleft = (x_button, y_button)	# placing topleft corner of image to wanted position
		self.clicked = False	# button is not clicked at the beginning
		#	TEXT
		font_size = text_size * width_screen
		image_height = self.image.get_height()
		self.font = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(font_size))	# loading font
		text_height = self.font.get_height()
		self.text_to_write = text
		self.x_text = x_button + (text_height/2)
		self.y_text = y_button + (image_height/2) - (text_height/2)

	def draw_button_and_text(self, surface):
		#	BUTTON
		action = False
		pos = pygame.mouse.get_pos()	# get mouse position
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
				self.clicked = True
			if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
				self.clicked = False
				action = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		surface.blit(self.image, (self.rect.x, self.rect.y))	# draw button on screen
		#	TEXT
		surface.blit(self.font.render(self.text_to_write, True, (40, 40, 40)), (self.x_text, self.y_text))

		return action

	def draw_button(self, surface):
		action = False
		pos = pygame.mouse.get_pos()	# get mouse position
		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		surface.blit(self.image, (self.rect.x, self.rect.y))	# draw button on screen

		return action