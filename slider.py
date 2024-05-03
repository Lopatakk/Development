import pygame
from screensetup import *

class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value_percent):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        # Initial value of the slider in percentage
        self.value = self.min_value + (initial_value_percent / 100) * (self.max_value - self.min_value)
        self.dragging = False  # Indicates whether the slider is being dragged by the mouse
        self.button_sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")
        self.button_music = pygame.mixer.Sound("assets/sounds/background_music_volume.mp3")

    def draw(self, screen):
        # Color of the slider background
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))
        # Color of the slider button
        pygame.draw.rect(screen, (230, 230, 230), (self.x, self.y, (self.value - self.min_value) / (self.max_value - self.min_value) * self.width, self.height))

    def update(self, mouse_pressed, settings, option):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        # If the mouse is over the slider and the left mouse button is pressed, start dragging the slider
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            if mouse_clicked:
                # If the slider is being dragged, update its value based on the mouse position
                self.dragging = True
                self.value = (mouse_pos[0] - self.x) / self.width * (self.max_value - self.min_value) + self.min_value
                self.value = max(self.min_value, min(self.max_value, self.value))
            else:
                # If the mouse button is released, stop dragging the slider
                self.dragging = False

            if mouse_pressed:
                settings[option] = self.value / 20
                with open("settings.json", "w") as settings_file:

                    json.dump(settings, settings_file, indent=4)
                ScreenSetup.update()

                if option == "music_volume":
                    pass
                    pygame.mixer.Channel(3).set_volume(0.04 * ScreenSetup.music_volume)
                    pygame.mixer.Channel(3).play(self.button_music, 1)
                else:
                    pygame.mixer.Channel(3).stop()
                    self.button_sound.set_volume(0.2 * ScreenSetup.effects_volume)
                    pygame.mixer.Channel(3).play(self.button_sound)


    def get_value_in_percent(self):
        return ((self.value - self.min_value) / (self.max_value - self.min_value)) * 100