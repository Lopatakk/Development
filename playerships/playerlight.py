from playership import PlayerShip
from pygame.sprite import Group
import json
import pygame
from projectile import Projectile
import numpy as np


class PlayerLight(PlayerShip):
    """
    Light, fast, agile, but fragile. Armed with 2 quite powerful cannons on the sides with slower fire rate this ship
    flies over the battlefield like a feather, thanks to its high acceleration and top speed. But be careful and try to
    avoid any contact with enemies and projectiles because you don't have much hp to lose.
    Q action: dash - quickly moves in the direction of pressed keys
    E action: shield - creates a shield around the ship, which protects it from enemy projectiles
    """
    def __init__(self, projectile_group: Group):
        """
        :param projectile_group: sprite group for fired projectiles
        """
        # reading parameters file and picking PlayerLight data from it
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[0]

        super().__init__("assets/images/vlod5L.png", param["type"], param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["proj_dmg"],
                         param["fire_rate"], param["cooling"], param["overheat"], param["q_cooldown"],
                         param["q_ongoing_time"], param["e_cooldown"], param["e_ongoing_time"], projectile_group)

        # q action variables and setup
        self.velocity_before = None

        # e action variables and setup
        self.hp_before = None
        self.image_non_rot_with_shield = pygame.image.load("assets/images/vlod5LS.png")
        self.image_non_rot_without_shield = self.image_non_rot
        self.shield_on_sound = pygame.mixer.Sound("assets/sounds/shield_on.mp3")
        self.shield_on_sound.set_volume(0.4)
        self.shield_off_sound = pygame.mixer.Sound("assets/sounds/shield_off.mp3")
        self.shield_off_sound.set_volume(0.6)

        # 2 cannon shooting setup
        self.proj_spawn_offset_1 = np.array([- 1/3 * self.width, - 1/4.5 * self.height])
        self.proj_spawn_offset_2 = np.array([+ 1/3 * self.width, - 1/4.5 * self.height])
        self.proj_spawn_offset = self.proj_spawn_offset_1

        # shooting animation setup
        self.shooting_images = []
        for num in range(1, 4):
            img = pygame.image.load(f"assets/animations/shooting/LIGHT/LIGHT{num}.png")
            # add the image to the list
            self.shooting_images.append(img)
        self.index = 0
        self.counter = -1
        self.animation_speed = 3

    def update(self):
        """
        Customized update function including shooting animation and shield functionality unlike the PlayerShip update.
        :return: None
        """
        # shooting animation
        if self.counter >= 0:
            self.counter += 1
        if self.counter >= self.animation_speed and self.index < len(self.shooting_images) - 1:
            # changing the picture
            self.counter = 0
            self.index += 1
            self.image_non_rot = self.shooting_images[self.index]
        if self.index >= len(self.shooting_images) - 1 and self.counter >= self.animation_speed:
            # end of the animation
            self.counter = -1
            self.index = 0
            self.image_non_rot = self.image_non_rot_without_shield
            # firing from left gun
            projectile = Projectile(self)
            self.projectile_group.add(projectile)
            self.proj_spawn_offset = self.proj_spawn_offset_2
            # firing from right gun
            projectile = Projectile(self)
            self.projectile_group.add(projectile)
            self.proj_spawn_offset = self.proj_spawn_offset_1

        super().update()

        # shield functionality
        if self.is_e_action_on:
            self.hp = self.hp_before

    def q_action(self):
        """
        Dash start, the ship is faster.
        :return: None
        """
        self.velocity_before = self.velocity
        self.acceleration = 30 * self.acceleration
        self.max_velocity = 30 * self.max_velocity

    def q_turn_off(self):
        """
        Dash end, the ship as fast as before the dash.
        :return: None
        """
        self.velocity = self.velocity_before
        self.acceleration = 1/30 * self.acceleration
        self.max_velocity = 1/30 * self.max_velocity

    def e_action(self):
        """
        Shield turn on, the ship now has a shield.
        :return: None
        """
        self.hp_before = self.hp
        self.image_non_rot = self.image_non_rot_with_shield
        self.image = self.image_non_rot
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        pygame.mixer.find_channel(True).play(self.shield_on_sound)

    def e_turn_off(self):
        """
        Shield turn off, the ship loses the shield.
        :return: None
        """
        self.hp = self.hp_before
        self.image_non_rot = self.image_non_rot_without_shield
        self.image = self.image_non_rot
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        pygame.mixer.find_channel(True).play(self.shield_off_sound)

    def shoot(self):
        """
        If the time after last shot is larger than self.fire_rate_time and the gun is not overheated, this function
        heats the guns and starts the shooting animation at which end there are created two projectiles.
        :return: None
        """
        elapsed_time = self.time_alive - self.last_shot_time
        if elapsed_time >= self.fire_rate_time and not self.is_overheated:
            self.last_shot_time = self.time_alive
            self.heat += 2

            self.counter = 0
            self.image_non_rot = self.shooting_images[self.index]
