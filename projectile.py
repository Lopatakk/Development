import pygame
import numpy as np
from screensetup import ScreenSetup


class Projectile(pygame.sprite.Sprite):
    """
    This class takes care of basic projectiles. Projectiles are fired from ships, so the constructor takes the ship as
    an input. Projectiles does not change its direction during its flight, it travels under the same angle until it
    reaches screen borders, where they are destroyed. They deal damage when they collide with ships (which is taken
    care of in collisions.py).
    """

    def __init__(self, ship):
        # Constructor creates a projectile itself with all the needed properties. It needs some properties from the ship
        # that fired it, so it takes the ship as an input.

        # super().__init__() - allows to use properties of Sprite, starts the code in Sprite constructor
        super().__init__()

        # image

        # This section loads the image and creates a rect and a mask out of it. It also uses the convert function to
        # improve performance. Mask is created, because we use mask collision system. If we did not create mask here,
        # the code would have to make mask everytime it checks for some collisions, which can lead to a decrease of
        # performance.
        self.image = pygame.image.load("assets/images/projectile.png")
        self.image = pygame.Surface.convert(self.image)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # start position

        # This section calculates the spawn position (the end of the ship) and sets its position here. It takes the
        # ship's coordinates as a base and then (because of pygame coordinates) subtracts half of the ship's width
        # multiplied by sin/cos of the ship's angle.
        self.posx = ship.rect.centerx - 1/2 * ship.ship_width * np.sin(np.deg2rad(ship.angle))
        self.posy = ship.rect.centery - 1/2 * ship.ship_width * np.cos(np.deg2rad(ship.angle))
        self.rect.center = [self.posx, self.posy]

        # angle

        # angle - the angle under which the projectile travels through space, it does not change, here it is set to the
        #   angle of the ship
        self.angle = ship.angle

        # velocity

        # velocity - the speed which the projectile travels through space, it does not change, it is used to calculate
        #   updated position of a projectile
        self.velocity = 15

        # damage

        # dmg - how much hp are taken from a ship if the ship collides with a projectile.
        self.dmg = ship.proj_dmg

    def update(self):
        """
        The update() function only updates the projectile's position from its angle and velocity, then sets its center
        to the new calculated position and if the projectile gets behind borders of the screen, the function kills it.
        """
        self.posx -= np.sin(np.deg2rad(self.angle)) * self.velocity
        self.posy -= np.cos(np.deg2rad(self.angle)) * self.velocity
        self.rect.center = [self.posx, self.posy]

        #  kill behind borders
        if self.posx > ScreenSetup.width or self.posx < 0 or self.posy > ScreenSetup.height or self.posy < 0:
            self.kill()
