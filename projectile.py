import pygame
import numpy as np
from screensetup import ScreenSetup


class Projectile(pygame.sprite.Sprite):
    """
    This class takes care of basic projectiles. Projectiles are fired from ships, so the constructor takes the ship as
    an input. Projectiles do not change its direction during its flight. They travel at the same angle until they reach
    screen borders, where they are destroyed. They do damage to ships when they collide with them (which is taken care
    of in collisions.py).
    """

    def __init__(self, ship):
        """
        Creates a projectile itself with all the needed properties.
        :param ship: The ship that fired the projectile
        """

        # super().__init__() - allows to use properties of Sprite, starts the code in Sprite constructor
        super().__init__()

        # angle

        # angle - the angle under which the projectile travels through space, it does not change, here it is set to the
        #   angle of the ship
        self.angle = ship.angle

        # image

        # This section loads the image and creates a rect and a mask out of it. It also uses the convert function to
        # improve performance. Mask is created because we use a mask collision system. If we did not create mask here,
        # the code would have to make mask every time it checks for some collisions, which can lead to a decrease of
        # performance.
        if ship.type.startswith("player"):
            self.image = pygame.image.load("assets/images/projectile.png")
        else:
            self.image = pygame.image.load("assets/images/projectilered.png")
        self.image = pygame.transform.scale_by(self.image, ScreenSetup.width / 1920)
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.image = pygame.Surface.convert_alpha(self.image)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # start position

        # This section calculates the spawn position (the end of the ship) and sets its position here. It takes the
        # ship's coordinates as a base and then (because of pygame coordinates) subtracts half of the ship's width
        # multiplied by sin/cos of the ship's angle.
        self.pos = np.array([ship.pos[0] + ship.proj_spawn_offset[1] * np.sin(np.deg2rad(ship.angle))
                             + ship.proj_spawn_offset[0] * np.cos(np.deg2rad(ship.angle)),
                             ship.pos[1] + ship.proj_spawn_offset[1] * np.cos(np.deg2rad(ship.angle))
                             - ship.proj_spawn_offset[0] * np.sin(np.deg2rad(ship.angle))])
        self.rect.center = self.pos

        # velocity

        # velocity - the speed which the projectile travels through space, it does not change, it is used to calculate
        #   the updated position of a projectile
        self.velocity = 15

        # damage

        # dmg - how much hp is taken from a ship if the ship collides with a projectile.
        self.dmg = ship.proj_dmg

        # sound of firing

        self.sound = pygame.mixer.Sound("assets/sounds/beam_shoot.mp3")  # Load sound file
        self.sound.set_volume(0.2)
        pygame.mixer.find_channel(False).play(self.sound)

        # other

        # type - indicates a projectile type, used in collisions
        self.type = "normal"

    def update(self):
        """
        The update() function only updates the projectile's position from its angle and velocity, then sets its center
        to the new calculated position, and if the projectile gets behind the borders of the screen, the function
        destroys it.
        :return: None
        """
        self.pos -= np.array([np.sin(np.deg2rad(self.angle)) * self.velocity,
                              np.cos(np.deg2rad(self.angle)) * self.velocity])
        self.rect.center = self.pos

        #  kill behind borders
        if self.pos[0] > ScreenSetup.width or self.pos[0] < 0 or self.pos[1] > ScreenSetup.height or self.pos[1] < 0:
            self.kill()

    def kill(self):
        """
        On the top of the original kill() function, it sets the mask to None, to be sure.
        :return: None
        """
        super().kill()
        self.mask = None
