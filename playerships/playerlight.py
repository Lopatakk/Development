from playership import PlayerShip
from pygame.sprite import Group
import json
import pygame


class PlayerLight(PlayerShip):
    def __init__(self, clock, projectile_group: Group):
        # reading parameters file and picking PlayerLight data from it
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[0]

        super().__init__("assets/images/vlod5L.png", param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["proj_dmg"],
                         param["fire_rate"], param["cooling"], param["overheat"], param["q_cooldown"],
                         param["q_ongoing_time"], param["e_cooldown"], param["e_ongoing_time"], projectile_group, clock)

        self.hp_before = None
        self.image_non_rot_with_shield = pygame.image.load("assets/images/vlod5LS.png")
        self.image_non_rot_without_shield = self.image_non_rot
        self.shield_on_sound = pygame.mixer.Sound("assets/sounds/shield_on.mp3")
        self.shield_on_sound.set_volume(0.4)
        self.shield_off_sound = pygame.mixer.Sound("assets/sounds/shield_off.mp3")
        self.shield_off_sound.set_volume(0.6)

    def update(self):
        super().update()
        if self.is_e_action_on:
            self.hp = self.hp_before

    def q_action(self):
        print("status quo")

    def q_turn_off(self):
        print("q turning off, over")

    def e_action(self):
        self.hp_before = self.hp
        self.image_non_rot = self.image_non_rot_with_shield
        self.image = self.image_non_rot
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        pygame.mixer.find_channel(True).play(self.shield_on_sound)

    def e_turn_off(self):
        self.hp_before = None
        self.image_non_rot = self.image_non_rot_without_shield
        self.image = self.image_non_rot
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        pygame.mixer.find_channel(True).play(self.shield_off_sound)
