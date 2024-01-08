import pygame
import json

class Button():
    def __init__(self, x_button, y_button, image_01_path, image_02_path, scale_w, scale_h, text_size, text, screen_in_button, sound_path, sound_volume):
        self.scale_w = scale_w
        self.scale_h = scale_h
        self.x_button = x_button
        self.y_button = y_button
        self.width_screen = screen_in_button.get_width()    # getting screen width
        self.clicked = False    # the button is not clicked at the beginning
        self.collision = False  # at the beginning, no collision occurs
        self.press = False      # the button cannot be pressed at the beginning
        self.mask_01_collision = False  # the is not anz collision with mouse and first mask at the beginning
        #	image_01
        self.image_01 = pygame.image.load(image_01_path).convert_alpha()  # load button image with transparency
        #	image_02
        self.image_02 = pygame.image.load(image_02_path).convert_alpha()  # load button image with transparency
        #	text
        font_size = text_size * self.width_screen
        self.font = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(font_size))  # loading font
        self.font_parameters = pygame.font.Font('assets/fonts/PublicPixel.ttf', int(font_size*0.5))  # loading font for ship parameters
        self.text_to_write = text
        #	sound
        self.sound = pygame.mixer.Sound(sound_path)  # Load sound file
        self.sound.set_volume(sound_volume)
        #   ship parameters
        # load information about ship from json
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        # selection of ship
        if image_01_path == "assets/images/vlod5L.png":
            self.Ship_param = player_param[0]
        elif image_01_path == "assets/images/vlod5.png":
            self.Ship_param = player_param[1]
        else:
            self.Ship_param = player_param[2]

    def draw_image_in_center(self, surface):
        action = False
        mouse_x, mouse_y = pygame.mouse.get_pos()  # get mouse position
        #   button
        # button_01
        image_01 = pygame.transform.scale(self.image_01, (int(self.width_screen * self.scale_w), int(self.width_screen * self.scale_h)))  # transforming image_01
        rect_01 = image_01.get_rect()  # creates a rectangular frame around the object's image_01
        rect_01.center = (self.x_button, self.y_button)  # placing center of image_01 to wanted position
        image_01_mask = pygame.mask.from_surface(image_01)  # mask from image_01
        # button_02
        image_02 = pygame.transform.scale(self.image_02, (int(self.width_screen * self.scale_w * 1.3), int(self.width_screen * self.scale_h * 1.3)))  # transforming image_02
        rect_02 = image_02.get_rect()  # creates a rectangular frame around the object's image_02
        rect_02.center = (self.x_button, self.y_button)  # placing center of image_02 to wanted position
        image_02_mask = pygame.mask.from_surface(image_02)  # mask from image_02
        #   selecting an image for interaction and display on the screen
        if not self.collision:  # image_01 is used for interaction and is displayed on screen
            surface.blit(image_01, rect_01)
            rect = rect_01
            mask = image_01_mask
            text_color = (150, 150, 150)
        else:
            surface.blit(image_02, rect_02) # image_02 is used for interaction and is displayed on screen
            rect = rect_02
            mask = image_02_mask
            text_color = (230, 230, 230)
        #   collision check
        # when this "if" is not there, there is a flicker between image_01 and image_02 on the interface
        if rect_01.collidepoint(mouse_x, mouse_y):
            offset_x_01 = mouse_x - rect_01.x
            offset_y_01 = mouse_y - rect_01.y
            if image_01_mask.get_at((offset_x_01, offset_y_01)):
                self.mask_01_collision = True
            else:
                self.mask_01_collision = False
        else:
            self.mask_01_collision = False
        # main collision check and action
        if rect.collidepoint(mouse_x, mouse_y):
            offset_x = mouse_x - rect.x
            offset_y = mouse_y - rect.y
            if mask.get_at((offset_x, offset_y)) or self.mask_01_collision == True:
                self.collision = True
                if pygame.mouse.get_pressed()[0] == 0:  # this makes it impossible to click outside the button and then hover over it and activate it without clicking
                    self.press = True
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked and self.press == 1:
                    self.clicked = True
                if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                    self.clicked = False
                    pygame.mixer.find_channel(True).play(self.sound)
                    action = True
            else:
                self.collision = False
                self.clicked = False
                self.press = False
        else:
            self.collision = False
            self.clicked = False
            self.press = False
        #   text
        text = self.font.render(self.text_to_write, True, text_color)
        text_rect = text.get_rect()
        text_rect.centerx = self.x_button
        text_rect.centery = self.y_button - (rect_02.height/2) * 1.3
        # draw text on screen
        surface.blit(text, text_rect)
        #   Printing ship parameters
        ship_text = [f"HP: {self.Ship_param['hp']}", f"DMG: {self.Ship_param['proj_dmg']}", f"Fire rate: {self.Ship_param['fire_rate']}", f"Acceleration: {self.Ship_param['acceleration']}", f"Speed: {self.Ship_param['max_velocity']}", "Q skill: " + self.Ship_param['q_skill'], "E skill: " + self.Ship_param['e_skill']]
        y_position = [self.y_button + (rect_02.height/2) * 1.3, self.y_button + (rect_02.height/2) * 1.6, self.y_button + (rect_02.height/2) * 1.9, self.y_button + (rect_02.height/2) * 2.2, self.y_button + (rect_02.height/2) * 2.5, self.y_button + (rect_02.height/2) * 2.8, self.y_button + (rect_02.height/2) * 3.1]
        for parameters, position in zip(ship_text, y_position):
            text = self.font_parameters.render(str(parameters), True, text_color)
            text_rect = text.get_rect()
            text_rect.centerx = self.x_button
            text_rect.centery = position
            # draw text on screen
            surface.blit(text, text_rect)

        return action

    def draw_button_and_text(self, surface):
        action = False
        mouse_x, mouse_y = pygame.mouse.get_pos()  # get mouse position
        #   button
        # button_01
        image_01 = pygame.transform.scale(self.image_01, (int(self.width_screen * self.scale_w), int(self.width_screen * self.scale_h)))  # transforming image_01
        rect_01 = image_01.get_rect()  # creates a rectangular frame around the object's image_01
        rect_01.topleft = (self.x_button, self.y_button)  # placing topleft corner of image_01 to wanted position
        image_01_mask = pygame.mask.from_surface(image_01)  # mask from image_01
        # button_02
        image_02 = pygame.transform.scale(self.image_02, (int(self.width_screen * self.scale_w), int(self.width_screen * self.scale_h)))  # transforming image_02
        rect_02 = image_02.get_rect()  # creates a rectangular frame around the object's image_02
        rect_02.topleft = (self.x_button, self.y_button)  # placing topleft corner of image_02 to wanted position
        image_02_mask = pygame.mask.from_surface(image_02)  # mask from image_02
        # selecting an image for interaction and display on the screen
        if not self.collision:  # image_01 is used for interaction and is displayed on screen
            surface.blit(image_01, rect_01)
            rect = rect_01
            mask = image_01_mask
            text_color = (40, 40, 40)
        else:
            surface.blit(image_02, rect_02) # image_02 is used for interaction and is displayed on screen
            rect = rect_02
            mask = image_02_mask
            text_color = (0, 0, 0)
        # collision check
        if rect.collidepoint(mouse_x, mouse_y):
            offset_x = mouse_x - rect.x
            offset_y = mouse_y - rect.y
            if mask.get_at((offset_x, offset_y)):
                self.collision = True
                if pygame.mouse.get_pressed()[0] == 0:  # this makes it impossible to click outside the button and then hover over it and activate it without clicking
                    self.press = True
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked and self.press == 1:
                    self.clicked = True
                if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                    self.clicked = False
                    pygame.mixer.find_channel(True).play(self.sound)
                    action = True
            else:
                self.collision = False
                self.clicked = False
                self.press = False
        else:
            self.collision = False
            self.clicked = False
            self.press = False
        #   text
        text = self.font.render(self.text_to_write, True, text_color)
        text_rect = text.get_rect()
        image_height = rect.height  # height of image
        text_height = text.get_height() # height of text
        text_rect.x = self.x_button + (text_height / 2)
        text_rect.y = self.y_button - (text_height / 2) + (image_height / 2)
        # draw text on screen
        surface.blit(text, text_rect)

        return action