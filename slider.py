import pygame
from gamesetup import *


class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value_percent, joystick, joystick_index):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.joystick = joystick
        self.joystick_index = joystick_index
        self.play_sound = False

        # Initial value of the slider in percentage
        self.value = self.min_value + (initial_value_percent / 100) * (self.max_value - self.min_value)
        self.dragging = False  # Indicates whether the slider is being dragged by the mouse
        self.button0 = pygame.image.load("assets/images/slider_button_black.png").convert_alpha()
        self.button1 = pygame.image.load("assets/images/slider_button_white.png").convert_alpha()
        new_width = int(self.button0.get_width() * 2.5)
        new_height = int(self.button0.get_height() * 2.5)
        self.button0 = pygame.transform.scale(self.button0, (new_width, new_height))
        self.button1 = pygame.transform.scale(self.button1, (new_width, new_height))
        self.button_rect = self.button0.get_rect()

    def draw(self, screen, on_language):
        # Color of the slider background
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))
        # Color of the slider button
        pygame.draw.rect(screen, (230, 230, 230), (self.x, self.y, (self.value * 5 - self.min_value) / (self.max_value - self.min_value) * self.width, self.height))
        # slider circle button
        self.button_rect.centerx = self.x + (self.value * 5 - self.min_value) / (self.max_value - self.min_value) * self.width
        self.button_rect.centery = self.y + self.height/2

        if self.joystick.active:
            if self.joystick.position == self.joystick_index and not on_language:
                screen.blit(self.button1, self.button_rect)
            else:
                screen.blit(self.button0, self.button_rect)
        else:
            if self.dragging:
                screen.blit(self.button1, self.button_rect)
            else:
                screen.blit(self.button0, self.button_rect)

    def update(self, settings, option, on_language):
        scroll = float(self.button_rect.centerx)
        if self.joystick.active and not on_language:
            if self.joystick.position == self.joystick_index:
                if abs(self.joystick.left_joystick[0]) > 0.2:
                    # if sliding, cannot move buttons
                    increment = 10 * self.joystick.left_joystick[0]
                    self.joystick.sliding = True
                else:
                    increment = 0
                    self.joystick.sliding = False
                scroll += increment
                if scroll < self.x:
                    scroll = self.x
                elif scroll > self.x + self.width:
                    scroll = self.x + self.width
                self.value = ((scroll - self.x) / self.width * (self.max_value - self.min_value) + self.min_value)
                self.value = max(self.min_value, min(self.max_value, self.value))
                self.value = self.value / 5

                # If the slider is being dragged, update its value based on button position,
                if self.joystick.sliding:
                    if option == "music_volume":
                        settings[option] = self.min_value + (self.get_value_in_percent() / 100) * (
                                    self.max_value - self.min_value)
                    else:
                        settings[option] = self.min_value + (self.get_value_in_percent() / 100) * (
                                    self.max_value - self.min_value)

                    with open("settings.json", "w") as settings_file:
                        json.dump(settings, settings_file, indent=4)
                    GameSetup.update()

                    if option == "music_volume":
                        pygame.mixer.Channel(3).set_volume(0.04 * GameSetup.music_volume)
                        if not pygame.mixer.Channel(3).get_busy():
                            pygame.mixer.Channel(3).play(GameSetup.button_music, 1)
                    else:
                        self.play_sound = True
                else:
                    if self.play_sound:
                        pygame.mixer.Channel(3).stop()
                        pygame.mixer.Channel(4).set_volume(0.2 * GameSetup.effects_volume)
                        if not pygame.mixer.Channel(4).get_busy():
                            pygame.mixer.Channel(4).play(GameSetup.button_sound)
                        self.play_sound = False

        else:
            # If the mouse is over the slider and the left mouse button is pressed, start dragging the slider
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]
            if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height or self.dragging:
                if mouse_clicked:
                    # If the slider is being dragged, update its value based on the mouse position
                    self.dragging = True
                    self.value = (mouse_pos[0] - self.x) / self.width * (self.max_value - self.min_value) + self.min_value
                    self.value = max(self.min_value, min(self.max_value, self.value))
                    self.value = self.value / 5
                else:
                    # If the mouse button is released, stop dragging the slider
                    self.dragging = False

            if self.dragging:
                if option == "music_volume":
                    settings[option] = self.min_value + (self.get_value_in_percent() / 100) * (self.max_value - self.min_value)
                else:
                    settings[option] = self.min_value + (self.get_value_in_percent() / 100) * (self.max_value - self.min_value)

                with open("settings.json", "w") as settings_file:
                    json.dump(settings, settings_file, indent=4)
                GameSetup.update()

                if option == "music_volume":
                    pygame.mixer.Channel(3).set_volume(0.04 * GameSetup.music_volume)
                    if not pygame.mixer.Channel(3).get_busy():
                        pygame.mixer.Channel(3).play(GameSetup.button_music, 1)
                else:
                    self.play_sound = True
            else:
                if self.play_sound:
                    pygame.mixer.Channel(3).stop()
                    pygame.mixer.Channel(4).set_volume(0.2 * GameSetup.effects_volume)
                    if not pygame.mixer.Channel(4).get_busy():
                        pygame.mixer.Channel(4).play(GameSetup.button_sound)
                    self.play_sound = False



    def get_value_in_percent(self):
        return ((self.value - self.min_value) / (self.max_value - self.min_value)) * 100

