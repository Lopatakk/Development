from enemy import Enemy
import numpy as np
import pygame
import random
from playership import PlayerShip
import json
from screensetup import ScreenSetup
from projectile import Projectile


class Sniper(Enemy):
    def __init__(self, start, projectile_group, player):
        # reading parameters file and picking Sniper data from it
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[2]

        super().__init__(start, "assets/images/sniper.png", param["type"], param["hp"], param["dmg"],
                         param["explosion_size"], param["max_velocity"], param["acceleration"],
                         param["velocity_coefficient"], param["rot_velocity"], param["proj_dmg"], param["fire_rate"],
                         param["cooling"], param["overheat"], param["offset"], projectile_group, player)
        self.proj_spawn_offset = np.array([0, - 1/1.95 * self.height])
        self.image_non_rot = pygame.transform.scale_by(self.image_non_rot, ScreenSetup.width/2800)
        self.rot_direction = random.choice([1, -1])

        # shooting animation setup
        self.image_non_rot_orig = self.image_non_rot
        self.shooting_images = []
        for num in range(1, 4):
            img = pygame.image.load(f"assets/animations/shooting/SNIPER/sniper{num}.png")
            img = pygame.transform.scale_by(img, ScreenSetup.width/2800)
            self.shooting_images.append(img)
        self.index = 0
        self.counter = -1
        self.animation_speed = 4

    def update(self):
        self.angle_speed(self.rot_direction)
        self.follow_movement_with_offset()
        self.shoot()

        # shooting animation
        if self.counter >= 0:
            self.counter += 1
        #   changing the picture
        if self.counter >= self.animation_speed and self.index < len(self.shooting_images) - 1:
            self.counter = 0
            self.index += 1
            self.image_non_rot = self.shooting_images[self.index]
        #   end of the animation
        if self.index >= len(self.shooting_images) - 1 and self.counter >= self.animation_speed:
            self.counter = -1
            self.index = 0
            self.image_non_rot = self.image_non_rot_orig
            # firing from the gun
            projectile = Projectile(self)
            self.projectile_group.add(projectile)

        super().update()

    def shoot(self):
        """
        If the time after last shot is larger than self.fire_rate_time and the gun is not overheated, this function
        heats the gun and starts the shooting animation by setting the counter to 0. At the end of the animation is
        created a projectile.
        :return: None
        """
        elapsed_time = self.time_alive - self.last_shot_time
        if elapsed_time >= self.fire_rate_time and not self.is_overheated:
            self.last_shot_time = self.time_alive
            self.heat += 1

            self.counter = 0
            self.image_non_rot = self.shooting_images[self.index]