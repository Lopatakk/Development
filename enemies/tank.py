from enemies.enemy import Enemy
import pygame
import numpy as np
import json
from screensetup import ScreenSetup


class Tank(Enemy):
    def __init__(self, start, projectile_group, player):
        # reading parameters file and picking Tank data from it
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[1]
        image = pygame.image.load("assets/images/enemy/tank/tank.png")
        image = self.scale_image(image)

        super().__init__(start, image, param["img_scaling_coefficient"], param["shooting_ani_images"],
                         param["type"], param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["rot_velocity"],
                         param["proj_dmg"], param["fire_rate"], param["cooling"], param["overheat"],
                         param["offset"], projectile_group, player)

        self.proj_spawn_offset = np.array([0, -1/2 * self.height])

        # static image
        self.damaged_images = []
        for i in range(4):
            damaged_image = pygame.image.load(f"assets/images/enemy/tank/tank_damaged{i}.png")
            damaged_image = self.scale_image(damaged_image)
            damaged_image = pygame.transform.scale_by(damaged_image, self.img_scale_ratio)
            self.damaged_images.append(damaged_image)

        # animation frames
        self.ani_shooting_images_damaged_array = []
        for i in range(4):
            ani_shooting_images_damaged = []
            for num in range(1, param["shooting_ani_images"] + 1):

                img = pygame.image.load(f"assets/animations/shooting/tank/tank{num}_damaged{i}.png").convert_alpha()
                img = pygame.transform.scale_by(img, self.img_scale_ratio)
                img = self.scale_image(img)
                ani_shooting_images_damaged.append(img)
            self.ani_shooting_images_damaged_array.append(ani_shooting_images_damaged)

    def update(self):
        # damaged appearance
        if self.hp < self.max_hp * 0.2:
            self.image_non_rot = self.damaged_images[3]
            self.ani_shooting_images = self.ani_shooting_images_damaged_array[3]
        elif self.hp < self.max_hp * 0.4:
            self.image_non_rot = self.damaged_images[2]
            self.ani_shooting_images = self.ani_shooting_images_damaged_array[2]
        elif self.hp < self.max_hp * 0.6:
            self.image_non_rot = self.damaged_images[1]
            self.ani_shooting_images = self.ani_shooting_images_damaged_array[1]
        elif self.hp < self.max_hp * 0.8:
            self.image_non_rot = self.damaged_images[0]
            self.ani_shooting_images = self.ani_shooting_images_damaged_array[0]

        # movement
        self.find_direction(self.player.pos)
        self.shoot()
        self.follow_movement(5)

        super().update()
