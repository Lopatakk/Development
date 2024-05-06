import pygame.mixer
from playerships.blast import Blast
from playerships.playership import PlayerShip
from pygame.sprite import Group
import json
from gamesetup import GameSetup


class PlayerMid(PlayerShip):
    """
    Middle classed ship with balanced properties. Not so light armor, quite good manoeuvrability and a relatively
    powerful gun results in a universal machine that can withstand some damage as well as fly away from its enemies and
    kill them while doing so. There is nothing to recommend you, try your best!
    Q action: rapid fire - increases fire rate and cooling
    E action: blast - fires a big projectile, which destroys everything in its path
    """
    def __init__(self, joystick, projectile_group: Group, mini=False, image=None, img_scaling_coefficient=None,
                 ani_amount_of_images=None, ship_type=None, hp=None, dmg=None, explosion_size=None,
                 regeneration=None, max_velocity=None, acceleration=None, velocity_coefficient=None,
                 proj_dmg=None, fire_rate=None, cooling=None, overheat=None,
                 q_cooldown=None, q_ongoing_time=None, e_cooldown=None,
                 e_ongoing_time=None) -> "PlayerShip":
        """
        :param projectile_group: sprite group for fired projectiles
        """
        # reading parameter file and picking PlayerMid data from it
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[1]
        if mini:
            super().__init__(joystick, image, img_scaling_coefficient, ani_amount_of_images, ship_type, hp,
                             dmg, explosion_size, regeneration, max_velocity, acceleration, velocity_coefficient,
                             proj_dmg, fire_rate, cooling, overheat, q_cooldown, q_ongoing_time, e_cooldown,
                             e_ongoing_time, mini, projectile_group)
        else:
            image = pygame.image.load("assets/images/player_mid/vlod_player_mid.png").convert_alpha()
            super().__init__(joystick, image, param["img_scaling_coefficient"], param["shooting_ani_images"],
                             param["type"], param["hp"], param["dmg"], param["explosion_size"], param["regeneration"],
                             param["max_velocity"], param["acceleration"], param["velocity_coefficient"],
                             param["proj_dmg"], param["fire_rate"], param["cooling"], param["overheat"],
                             param["q_cooldown"], param["q_ongoing_time"], param["e_cooldown"], param["e_ongoing_time"],
                             mini, projectile_group)

        # q action variables and setup
        self.gun_upgrade_sound = pygame.mixer.Sound("assets/sounds/gun_upgrade.mp3")
        self.gun_upgrade_sound.set_volume(0.6 * GameSetup.effects_volume)

    def update(self):
        """
        Customized update function including shooting animation unlike the PlayerShip update.
        :return: None
        """
        super().update()

    def q_action(self):
        """
        Rapid fire start, the ship can shoot more often, cooling is increased, shooting animation speed increased.
        :return: None
        """

        for module, level in self.ship_parts.items():
            if module == 'weapons':
                self.fire_rate_time = 1 / self.fire_rate_array[level] / 2
                self.cooling = self.cooling_array[level] / 60 * 4
                self.ani_speed -= 1
                self.gun_upgrade_sound.set_volume(0.6 * GameSetup.effects_volume)
                pygame.mixer.find_channel(False).play(self.gun_upgrade_sound)

    def q_turn_off(self):
        """
        Rapid fire end, the ship can shoot, cool the gun and run the shooting animation as fast as before.
        :return: None
        """

        for module, level in self.ship_parts.items():
            if module == 'weapons':
                self.fire_rate_time = 1/self.fire_rate_array[level]
                self.cooling = self.cooling_array[level]/60
                self.ani_speed += 1

    def e_action(self):
        """
        Blast shoot, fires the blast.
        :return: None
        """
        blast = Blast(self)
        self.projectile_group.add(blast)

    def e_turn_off(self):
        """
        Blast gets destroyed at the borders of the screen, E turn-off function does not have to do anything here.
        :return: None
        """
        pass

