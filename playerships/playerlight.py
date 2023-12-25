from playership import PlayerShip
from pygame.sprite import Group
import json
import pygame
from projectile import Projectile
import numpy as np


class PlayerLight(PlayerShip):
    def __init__(self, projectile_group: Group):
        # reading parameters file and picking PlayerLight data from it
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[0]

        super().__init__("assets/images/vlod5L.png", param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["proj_dmg"],
                         param["fire_rate"], param["cooling"], param["overheat"], param["q_cooldown"],
                         param["q_ongoing_time"], param["e_cooldown"], param["e_ongoing_time"], projectile_group)

        self.proj_spawn_offset_1 = np.array([- 1/3 * self.width, - 1/4.5 * self.height])
        self.proj_spawn_offset_2 = np.array([+ 1/3 * self.width, - 1/4.5 * self.height])
        self.proj_spawn_offset = self.proj_spawn_offset_1

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

    def shoot(self):
        """
        If the time after last shot is greater than fire_rate_time and the gun is not overheated, this function creates
        (spawns) a projectile and adds it to the projectile group.
        """
        elapsed_time = self.time_alive - self.last_shot_time
        if elapsed_time >= self.fire_rate_time and not self.is_overheated:
            projectile = Projectile(self)
            self.projectile_group.add(projectile)
            self.proj_spawn_offset = self.proj_spawn_offset_2

            projectile = Projectile(self)
            self.projectile_group.add(projectile)
            self.proj_spawn_offset = self.proj_spawn_offset_1

            self.last_shot_time = self.time_alive
            self.heat += 2
