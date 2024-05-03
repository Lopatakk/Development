from enemies.enemy import Enemy
import numpy as np
import pygame
import random
import json
from screensetup import ScreenSetup


class Sniper(Enemy):
    def __init__(self, start, projectile_group, player):
        # reading parameters file and picking Sniper data from it
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[2]
        image = pygame.image.load("assets/images/enemy/sniper/sniper.png")
        image = self.scale_image(image)

        super().__init__(start, image, param["img_scaling_coefficient"], param["shooting_ani_images"],
                         param["type"], param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["rot_velocity"],
                         param["proj_dmg"], param["fire_rate"], param["cooling"], param["overheat"],
                         param["offset"], False, projectile_group, player)

        self.proj_spawn_offset = np.array([0, -1/2 * self.height])
        self.rot_direction = random.choice([1, -1])

        # static image
        self.damaged_image = pygame.image.load(f"assets/images/enemy/sniper/sniper_damaged.png")
        self.damaged_image = self.scale_image(self.damaged_image)
        self.damaged_image = pygame.transform.scale_by(self.damaged_image, self.img_scale_ratio)

        # animation frames
        self.ani_shooting_images_damaged = []
        for num in range(1, param["shooting_ani_images"] + 1):

            img = pygame.image.load(f"assets/animations/shooting/sniper/sniper_damaged{num}.png").convert_alpha()
            img = pygame.transform.scale_by(img, self.img_scale_ratio)
            img = self.scale_image(img)
            self.ani_shooting_images_damaged.append(img)

    def update(self):
        # damaged appearance
        if self.hp < self.max_hp / 2:
            self.image_non_rot = self.damaged_image
            self.ani_shooting_images = self.ani_shooting_images_damaged

        # movement
        self.find_direction(self.player.pos)
        self.angle_speed(self.rot_direction)
        self.follow_movement_with_offset()
        self.shoot()

        super().update()
