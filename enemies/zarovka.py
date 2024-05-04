from enemies.enemy import Enemy
import pygame
import json


class Zarovka(Enemy):
    def __init__(self, start, player, mini=False, image=None, img_scaling_coefficient=None,
                 ani_amount_of_images=None, ship_type=None, hp=None, dmg=None, explosion_size=None,
                 max_velocity=None, acceleration=None, velocity_coefficient=None,
                 rot_velocity=None, proj_dmg=None, fire_rate=None, cooling=None, overheat=None,
                 offset=None):
        # reading parameters file and picking Zarovka data from it
        with open("enemies/enemyparams.json", "r") as param_file:
            enemy_param = json.load(param_file)
        param = enemy_param[0]
        if mini:
            super().__init__(start, image, img_scaling_coefficient, ani_amount_of_images, ship_type, hp,
                             dmg, explosion_size, max_velocity, acceleration, velocity_coefficient, rot_velocity,
                             proj_dmg, fire_rate, cooling, overheat, offset, mini, None, player)
        else:
            image = pygame.image.load("assets/images/enemy/zarovka/zarovka.png").convert_alpha()
            image = self.scale_image(image)
            super().__init__(start, image, param["img_scaling_coefficient"], param["shooting_ani_images"],
                             param["type"], param["hp"], param["dmg"], param["explosion_size"],
                             param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["rot_velocity"],
                             param["proj_dmg"], param["fire_rate"], param["cooling"], param["overheat"],
                             param["offset"], mini, None, player)

        self.damaged_images = []
        for i in range(2):
            damaged_image = pygame.image.load(f"assets/images/enemy/zarovka/zarovka_damaged{i}.png")
            damaged_image = self.scale_image(damaged_image)
            damaged_image = pygame.transform.scale_by(damaged_image, self.img_scale_ratio)
            self.damaged_images.append(damaged_image)

    def update(self):
        # damaged appearance
        if not self.mini:
            if self.hp < self.max_hp * 1/3:
                self.image_non_rot = self.damaged_images[1]
            elif self.hp < self.max_hp * 2/3:
                self.image_non_rot = self.damaged_images[0]

        # movement
        self.find_direction(self.player.pos)
        self.follow_movement(5)
        super().update()
