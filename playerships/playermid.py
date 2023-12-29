import pygame.mixer
from playerships.blast import Blast
from playership import PlayerShip
from pygame.sprite import Group
import json
from projectile import Projectile


class PlayerMid(PlayerShip):
    """
    Middle classed ship with balanced properties. Not so light armor, quite good manoeuvrability and a relatively
    powerful gun results in a universal machine that can withstand some damage as well as fly away from its enemies and
    killing them while doing so.w
    """
    def __init__(self, projectile_group: Group):
        # reading parameter file and picking PlayerMid data from it
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[1]

        super().__init__("assets/images/vlod5.png", param["type"], param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"], param["proj_dmg"],
                         param["fire_rate"], param["cooling"], param["overheat"], param["q_cooldown"],
                         param["q_ongoing_time"], param["e_cooldown"], param["e_ongoing_time"], projectile_group)

        self.gun_upgrade_sound = pygame.mixer.Sound("assets/sounds/gun_upgrade.mp3")
        self.gun_upgrade_sound.set_volume(0.6)

        # shooting animation
        self.image_non_rot_orig = self.image_non_rot
        self.shooting_images = []
        for num in range(1, 3):
            img = pygame.image.load(f"assets/animations/shooting/MID/MID{num}.png")
            # add the image to the list
            self.shooting_images.append(img)
        self.index = 0
        self.counter = -1
        self.animation_speed = 3

    def update(self):
        # shooting animation
        if self.counter >= 0:
            self.counter += 1
        if self.counter >= self.animation_speed and self.index < len(self.shooting_images) - 1:
            if self.is_q_action_on:
                self.index += 1
            else:
                self.counter = 0
                self.index += 1
                self.image_non_rot = self.shooting_images[self.index]
        if self.index >= len(self.shooting_images) - 1 and self.counter >= self.animation_speed:
            self.counter = -1
            self.index = 0
            self.image_non_rot = self.image_non_rot_orig

            projectile = Projectile(self)
            self.projectile_group.add(projectile)

        super().update()

    def q_action(self):
        self.fire_rate_time = self.fire_rate_time / 2
        self.cooling = self.cooling * 2.5
        pygame.mixer.find_channel(True).play(self.gun_upgrade_sound)

    def q_turn_off(self):
        self.fire_rate_time = self.fire_rate_time * 2
        self.cooling = self.cooling / 2.5

    def e_action(self):
        blast = Blast(self)
        self.projectile_group.add(blast)

    def e_turn_off(self):
        pass

    def shoot(self):
        """
        If the time after last shot is greater than fire_rate_time and the gun is not overheated, this function creates
        (spawns) a projectile and adds it to the projectile group.
        """
        elapsed_time = self.time_alive - self.last_shot_time
        if elapsed_time >= self.fire_rate_time and not self.is_overheated:
            self.last_shot_time = self.time_alive
            self.heat += 1

            self.counter = 0
            self.image_non_rot = self.shooting_images[self.index]
