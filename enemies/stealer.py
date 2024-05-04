from enemies.enemy import Enemy
import pygame
import json


class Stealer(Enemy):
    def __init__(self, start, player, item):
        # reading parameters file and picking Zarovka data from it
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[3]
        image = pygame.image.load("assets/images/enemy/stealer/stealer1.png")
        image = self.scale_image(image)
        self.took_item = False

        super().__init__(start, image, param["img_scaling_coefficient"], param["shooting_ani_images"],
                         param["type"], param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["rot_velocity"],
                         param["proj_dmg"], param["fire_rate"], param["cooling"], param["overheat"],
                         param["offset"], False, None, player)

        self.item = item
        self.image_non_rot_orig_with_medkit = pygame.image.load("assets/images/enemy/stealer/stealer2.png")
        self.image_non_rot_orig_with_medkit = pygame.transform.scale_by(self.image_non_rot_orig_with_medkit, self.img_scale_ratio)
        self.image_non_rot_orig_with_medkit = self.scale_image(self.image_non_rot_orig_with_medkit)
        self.image_non_rot_orig_with_medkit = pygame.Surface.convert_alpha(self.image_non_rot_orig_with_medkit)

        self.damaged_images = []
        for i in range(2):
            damaged_image = pygame.image.load(f"assets/images/enemy/stealer/stealer_damaged{i+1}.png")
            damaged_image = self.scale_image(damaged_image)
            damaged_image = pygame.transform.scale_by(damaged_image, self.img_scale_ratio)
            self.damaged_images.append(damaged_image)

    def update(self):
        # damaged appearance
        if self.hp < self.max_hp / 2:
            if self.took_item:
                self.image_non_rot = self.damaged_images[1]
            else:
                self.image_non_rot = self.damaged_images[0]

        # movement
        if self.item.alive():
            self.find_direction(self.item.pos)
            self.item_follow(self.item.pos)
        else:
            self.find_direction(self.player.pos)
            self.follow_movement(5)
        super().update()
