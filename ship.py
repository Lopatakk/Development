import pygame
import numpy as np
from projectile import Projectile
import time
from pygame.sprite import Group
from screensetup import ScreenSetup


class Ship(pygame.sprite.Sprite):
    """
    Parent class for creating ships (either player or enemy)
    Has basic properties (variables and functions)

    To use the properties from here in your child class, use super().__init__() function in constructor
    and super().update() in update() function. Note: Fill in the arguments in super().__init__() function
    (in the __init__() brackets). These are kinda intuitive (the confusing ones are explained in arguments notes).

    To move the ship change its velocity before calling the super().update() function. Position is then calculated
    automatically based on the velocity.
    Rotation is made semi-automatically. Just change the variable angle before calling the super().update() function
    to make the ship rotate.
    """

    def __init__(self, picture_path: str, start_pos: np.ndarray, max_velocity: int, velocity_coefficient: float,
                 hp: int, dmg: int, fire_rate: float, proj_dmg: int, projectile_group: Group, overheat: int, cooling: float,
                 explosion_size: int):
        """
        :param picture_path: directory path to the picture
        :param start_pos: starting position
        :param max_velocity: maximum speed the ship can travel
        :param velocity_coefficient: slows down the movement
        :param hp: maximum amount of health points
        :param dmg: damage when ramming
        :param fire_rate: how many projectiles can be fired in one second
        :param proj_dmg: damage of fired projectile
        :param overheat: maximum amount of heat the gun can stand
        :param cooling: how much of the heat the gun looses every second
        :param projectile_group: sprite group for fired projectiles
        """
        # Creates the ship itself with all the needed properties:

        # super().__init__() - allows to use properties of Sprite, starts the code in Sprite constructor
        super().__init__()

        # health

        # hp - health points of the ship, if it goes <= 0, the ship is killed
        self.hp = hp
        # max_hp
        self.max_hp = hp

        # image

        # image_non_rot - original, not-rotated picture of the ship (when rotating an image, it is necessary to use the
        #   original image as the image to be rotated, because when using an already rotated image, the resulting image
        #   is distorted)
        self.image_non_rot = pygame.image.load(picture_path)
        # image - realtime image of the ship, here it just gets uploaded and converted (the convert_alpha() (and
        #   convert()) function improves performance by faster blitting the images (I don't know anything about it))
        self.image = pygame.image.load(picture_path)
        self.image = pygame.Surface.convert_alpha(self.image)
        # rect - Sprites work with rectangles, it is one of the necessary things, here it gets created from the image
        self.rect = self.image.get_rect()
        # ship_width - variable used for calculating spawning point of projectiles, here it is equal to height of the
        #   ship, because the ship image is facing upwards
        self.ship_width = self.rect.height
        # mask - creates mask from partially transparent ship image, used for calculating precise collisions, the mask
        #   is then automatically updated in update()
        self.mask = pygame.mask.from_surface(self.image)

        # position

        # pos - numpy array of the ship position [x, y], it automatically changes in the update() based on velocity
        self.pos = start_pos

        # angle

        # angle - angle of rotation of the ship, it is 0, when the ship is facing upwards, it is not automatically
        #   changed in the update(), it has to be defined in the update() of the child class before calling the
        #   super().update() function
        self.angle = 0

        # velocity

        # velocity - array carrying the values of the ship speed in both axes [x, y], this is the one thing to change
        self.velocity = np.array([0, 0])
        # max_velocity - maximum speed of the ship, it is automatically checked, if it is exceeded or not
        self.max_velocity = max_velocity
        # velocity_coefficient - it is used for calculating the position, changes the ship's acceleration,
        #   it creates the smoother flow of controlling player's ship as well as allowing better (more detailed)
        #   range of speed of the ship
        self.velocity_coefficient = velocity_coefficient

        # spawn point

        # This sets the ship center at values defined when calling the constructor
        self.rect.center = self.pos

        # shooting

        # dmg - variable containing ship's ram damage
        self.dmg = dmg
        # proj_dmg - variable containing ship's projectile damage
        self.proj_dmg = proj_dmg
        # fire_rate_time - minimal time between firing two projectiles
        self.fire_rate_time = 1/fire_rate
        # last_shot_time - the time when the last shot was fired, used to decide if new projectile could be fired or not
        self.last_shot_time = time.time()
        # projectile_group - sprite group for storing projectiles
        self.projectile_group = projectile_group

        # gun overheating

        # heat - variable containing how much is the ship's gun heated
        self.heat = 0
        # overheat - maximum value of heat, if the heat reaches overheat, then the ship cannot fire
        self.overheat = overheat
        # cooling - how quickly the gun cools down, self.cooling = how much heat the gun looses every frame,
        #   cooling (the constructor's argument) = how much heat the gun looses every second
        self.cooling = cooling/60

        # explosion

        # explosion_size - size of an explosion after the ship is destroyed
        self.explosion_size = explosion_size

    def update(self):
        """
        The update() function updates the ships position and angle based on the ships velocity and angle variables. It
        also limits the ships velocity to its maximum value.
        It is not recommended to change the position variable directly.
        """

        # rotation
        # Variable angle must be calculated before calling the super().update() function!

        # This section rotates the ship's image according to variable angle. If angle == 0, then the ship is
        # facing upwards. Is also updates the ship's rect and the ship's mask based on the rotated image.
        self.image = pygame.transform.rotate(self.image_non_rot, self.angle)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # max speed limitations

        # This section is making sure the maximum defined velocity of the ship is not exceeded in both axes and both
        # directions. If it is exceeded, then it sets the velocity to its maximum value.
        # X
        if self.velocity[0] > self.max_velocity:
            self.velocity[0] = self.max_velocity
        elif self.velocity[0] < -self.max_velocity:
            self.velocity[0] = -self.max_velocity
        # Y
        if self.velocity[1] > self.max_velocity:
            self.velocity[1] = self.max_velocity
        elif self.velocity[1] < -self.max_velocity:
            self.velocity[1] = -self.max_velocity

        # movement

        # This section changes position of the ship based on its current velocity and velocity coefficient.
        self.pos[0] += self.velocity[0] * self.velocity_coefficient
        self.pos[1] += self.velocity[1] * self.velocity_coefficient

        # position update

        # This section has to be the last one, because it sets the ship on the new coordinates, that were calculated.
        self.rect.center = self.pos

        # gun cooling (overheat regeneration)

        # This section cools down the gun (if it's hot or warm)
        if self.heat > 0:
            self.heat -= self.cooling
        else:
            self.heat = 0

    @classmethod
    def rot_compute(cls, dist_x: int, dist_y: int):
        """
        This function calculates the angle based on the distances in the x and y axes. It is not limited to an object,
        it can be used anywhere. The input is the x-axis and y-axis distance. Non-absolute values must be used for the
        calculation, otherwise the angle cannot be calculated correctly. The output of the function is an integer in the
        interval <-90; 270). The function gives 0, when dist_y > 0 and dist_x == 0.
        """
        if dist_y > 0:
            return np.rad2deg(np.arctan(dist_x/dist_y))
        elif dist_y < 0:
            return 180 + np.rad2deg(np.arctan(dist_x/dist_y))
        else:
            if dist_x > 0:
                return 90
            else:
                return -90

    def shoot(self):
        """
        If the time after last shot is greater than fire_rate_time and the gun is not overheated, this function creates
        (spawns) a projectile and adds it to the projectile group.
        """
        elapsed_time = time.time() - self.last_shot_time
        if elapsed_time >= self.fire_rate_time and self.heat < self.overheat:
            projectile = Projectile(self)
            self.last_shot_time = time.time()
            self.projectile_group.add(projectile)
            self.heat += 1
