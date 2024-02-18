import pygame.mixer
from playerships.blast import Blast
from playership import PlayerShip
from pygame.sprite import Group
import json
from projectile import Projectile
from screensetup import ScreenSetup


class PlayerMid(PlayerShip):
    """
    Middle classed ship with balanced properties. Not so light armor, quite good manoeuvrability and a relatively
    powerful gun results in a universal machine that can withstand some damage as well as fly away from its enemies and
    kill them while doing so. There is nothing to recommend you, try your best!
    Q action: rapid fire - increases fire rate and cooling
    E action: blast - fires a big projectile, which destroys everything in its path
    """
    def __init__(self, projectile_group: Group):
        """
        :param projectile_group: sprite group for fired projectiles
        """
        # reading parameter file and picking PlayerMid data from it
        with open("playerships/playerparams.json", "r") as param_file:
            player_param = json.load(param_file)
        param = player_param[1]

        super().__init__("assets/images/vlod5.png", param["shooting_ani_images"], param["type"],
                         param["hp"], param["dmg"], param["explosion_size"],
                         param["max_velocity"], param["acceleration"], param["velocity_coefficient"],
                         param["proj_dmg"], param["fire_rate"], param["cooling"], param["overheat"],
                         param["q_cooldown"], param["q_ongoing_time"], param["e_cooldown"], param["e_ongoing_time"],
                         projectile_group)

        # q action variables and setup
        self.gun_upgrade_sound = pygame.mixer.Sound("assets/sounds/gun_upgrade.mp3")
        self.gun_upgrade_sound.set_volume(0.6 * ScreenSetup.effects_volume)

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
        self.fire_rate_time = self.fire_rate_time / 2
        self.cooling = self.cooling * 2.5
        self.ani_speed -= 1
        pygame.mixer.find_channel(False).play(self.gun_upgrade_sound)

    def q_turn_off(self):
        """
        Rapid fire end, the ship can shoot, cool the gun and run the shooting animation as fast as before.
        :return: None
        """
        self.fire_rate_time = self.fire_rate_time * 2
        self.cooling = self.cooling / 2.5
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
