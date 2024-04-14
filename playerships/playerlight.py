from playerships.playership import PlayerShip
from pygame.sprite import Group
import json
import pygame
from projectile import Projectile
import numpy as np
from screensetup import ScreenSetup


class PlayerLight(PlayerShip):
    """
    Light, fast, agile, but fragile. Armed with two cannons on the sides with slower fire rate, but quite good damage,
    this ship flies over the battlefield like a feather, thanks to its high acceleration and top speed. But be careful
    and try to avoid any contact with enemies and projectiles because you have only little hp to lose.
    Q action: dash - quickly moves in the direction of pressed keys
    E action: shield - creates a shield around the ship, which protects it from enemy projectiles
    """
    def __init__(self, projectile_group: Group):
        """
        :param projectile_group: sprite group for fired projectiles
        """
        # reading parameter file and picking PlayerLight data from it
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[0]

        super().__init__("assets/images/vlod5L.png", param["img_scaling_coefficient"], param["shooting_ani_images"],
                         param["type"], param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"],
                         param["proj_dmg"], param["fire_rate"], param["cooling"], param["overheat"],
                         param["q_cooldown"], param["q_ongoing_time"], param["e_cooldown"], param["e_ongoing_time"],
                         projectile_group)

        # q action variables and setup
        self.velocity_before = None

        # e action variables and setup
        self.hp_before = None
        self.image_non_rot_with_shield = pygame.image.load("assets/images/vlod5LS.png")
        self.image_non_rot_with_shield = pygame.transform.scale_by(self.image_non_rot_with_shield, self.img_scale_ratio)
        self.ani_shooting_images_with_shield = []
        # loading, scaling and converting animation images
        for num in range(1, len(self.ani_shooting_images)):
            img = pygame.image.load(f"assets/animations/shooting/{self.type}/{self.type}S{num}.png")
            img = pygame.transform.scale_by(img, self.img_scale_ratio)
            img = pygame.Surface.convert_alpha(img)
            self.ani_shooting_images_with_shield.append(img)
        self.ani_shooting_images_without_shield = self.ani_shooting_images
        self.image_non_rot_without_shield = self.image_non_rot
        self.shield_on_sound = pygame.mixer.Sound("assets/sounds/shield_on.mp3")
        self.shield_on_sound.set_volume(0.6 * ScreenSetup.effects_volume)
        self.shield_off_sound = pygame.mixer.Sound("assets/sounds/shield_off.mp3")
        self.shield_off_sound.set_volume(0.7 * ScreenSetup.effects_volume)

        # 2-cannon shooting setup
        self.proj_spawn_offset_1 = np.array([- 1/3 * self.width, - 1/5.5 * self.height])
        self.proj_spawn_offset_2 = np.array([+ 1/3 * self.width, - 1/5.5 * self.height])
        self.proj_spawn_offset = self.proj_spawn_offset_1

    def update(self):
        """
        Customized update function including shooting animation and shield functionality unlike the PlayerShip update.
        :return: None
        """
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
        self.image_non_rot_orig = self.image_non_rot_with_shield
        self.image_non_rot = self.image_non_rot_with_shield
        self.ani_shooting_images = self.ani_shooting_images_with_shield
        self.image = self.image_non_rot
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        pygame.mixer.find_channel(False).play(self.shield_on_sound)

    def e_turn_off(self):
        """
        Shield turn off, the ship loses the shield.
        :return: None
        """
        self.hp = self.hp_before
        self.image_non_rot_orig = self.image_non_rot_without_shield
        self.image_non_rot = self.image_non_rot_without_shield
        self.ani_shooting_images = self.ani_shooting_images_without_shield
        self.image = self.image_non_rot
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        pygame.mixer.find_channel(False).play(self.shield_off_sound)

    def fire(self) -> Projectile:
        # rewrote because of the 2-cannon setup
        projectile_1 = Projectile(self)
        projectile_1.sound.stop()
        self.proj_spawn_offset = self.proj_spawn_offset_2
        projectile_2 = Projectile(self)
        self.proj_spawn_offset = self.proj_spawn_offset_1
        return iter([projectile_1, projectile_2])
