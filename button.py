import pygame

class Button():
	def __init__(self, x_button, y_button, image_01_path, image_02_path, scale_w, scale_h, text_size, text, screen_in_button, sound_path, sound_volume):
		width_screen = screen_in_button.get_width()
		#	button_01
		image_01 = pygame.image.load(image_01_path).convert_alpha()	# load button images with transparency
		self.image_01 = pygame.transform.scale(image_01, (int(width_screen * scale_w), int(width_screen * scale_h)))	# transforming image_01
		self.rect = self.image_01.get_rect()	# creates a rectangular frame around the object's image_01
		self.rect.topleft = (x_button, y_button)	# placing topleft corner of image_01 to wanted position
		self.clicked = False	# button is not clicked at the beginning
		#	button_02
		image_02 = pygame.image.load(image_02_path).convert_alpha()  # load button images with transparency
		self.image_02 = pygame.transform.scale(image_02, (int(width_screen * scale_w), int(width_screen * scale_h)))  # transforming image_01
		#	text
		font_size = text_size * width_screen
		image_height = self.image_01.get_height()
		self.font = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(font_size))	# loading font
		text_height = self.font.get_height()
		self.text_to_write = text
		self.x_text = x_button + (text_height/2)
		self.y_text = y_button + (image_height/2) - (text_height/2)
		#	sound
		self.sound = pygame.mixer.Sound(sound_path)  # Load sound file
		self.sound.set_volume(sound_volume)

	def draw_button_and_text(self, surface):
		#	button
		action = False
		text_color = (40, 40, 40)
		image_button = self.image_01
		pos = pygame.mouse.get_pos()	# get mouse position

		if self.rect.collidepoint(pos):
			text_color = (0, 0, 0)
			image_button = self.image_02
			if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
				self.clicked = True
			if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
				self.clicked = False
				pygame.mixer.find_channel(True).play(self.sound)
				action = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		#	draw button on screen
		surface.blit(image_button, (self.rect.x, self.rect.y))
		#	draw text on screen
		surface.blit(self.font.render(self.text_to_write, True, (text_color)), (self.x_text, self.y_text))

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
		surface.blit(self.image_01, (self.rect.x, self.rect.y))	# draw button on screen

		return action