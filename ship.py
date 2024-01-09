import pygame
import numpy as np
from projectile import Projectile
from pygame.sprite import Group


class Ship(pygame.sprite.Sprite):
    """
    Parent class for creating ships (either player or enemy), based on the Sprite class from pygame.
    Includes basic properties, such as movement, shooting, etc.

    To move and rotate the ship change its velocity (recommended is by using the acceleration variable) and angle before
    calling the super().update() function. Position is then calculated automatically based on the velocity.
    """

    def __init__(self, start_pos: np.ndarray, picture_path: str, ship_type: str, hp: int, dmg: int, explosion_size: int,
                 max_velocity: float, acceleration: float, velocity_coefficient: float, proj_dmg: int, fire_rate: float,
                 cooling: float, overheat: int, projectile_group: Group) -> "Ship":
        """
        Creates a ship with all the needed properties:
        :param start_pos: spawning position of the ship
        :param picture_path: directory path to the ship picture
        :param ship_type: type of the ship
        :param hp: maximum amount of health points
        :param dmg: damage to other ships when ramming
        :param explosion_size: the size of the explosion when the ship is destroyed (see explosion.py for more)
        :param max_velocity: maximum speed the ship can travel in one axis
        :param acceleration: acceleration of the ship, is not used directly in the Ship class, but when defying movement functions in child class
        :param velocity_coefficient: enables greater range of speed, recommended value: 0.1
        :param proj_dmg: fired projectiles damage
        :param fire_rate: how many projectiles can be fired in one second
        :param cooling: how much of the heat the gun looses every second
        :param overheat: maximum amount of heat the gun can stand
        :param projectile_group: sprite group for fired projectiles
        :return: a Ship object
        """

        # super().__init__() - allows to use properties of Sprite, starts the code in Sprite constructor
        super().__init__()

        # type

        # type - type of the ship, used for deciding item collisions
        self.type = ship_type

        # health

        # hp - health points of the ship
        self.hp = hp
        # max_hp - maximum number of health points
        self.max_hp = hp

        # time

        # time_alive - in-game time the ship is alive (in seconds), used to calculate fire rate
        self.time_alive = 0

        # image

        # image_non_rot - original, not-rotated picture of the ship, facing upwards (when rotating an image, it is
        #                 necessary to use the original image as the image to be rotated, because, when using an already
        #                 rotated image, the resulting image is distorted)
        self.image_non_rot = pygame.image.load(picture_path)
        # image - realtime image of the ship, here it gets uploaded and converted (the convert_alpha() and convert()
        #         function improves performance by enabling faster rendering of the images)
        self.image = pygame.image.load(picture_path)
        self.image = pygame.Surface.convert_alpha(self.image)
        # rect - sprites work with rectangles, it is one of the necessary things, is created from the ship image
        self.rect = self.image.get_rect()
        # height - height of the image, used for calculating spawning point of projectiles and position of enemy health
        #          bar
        self.height = self.rect.height
        # width - width of the image, used for calculating spawning point of projectiles and position of enemy health
        #         bar
        self.width = self.rect.width
        # mask - creates mask from partially transparent ship image, used for calculating precise collisions, is updated
        #        every frame in update()
        self.mask = pygame.mask.from_surface(self.image)

        # position

        # pos - numpy array with [x, y] position of the ship center, changes in the update() based on velocity, respects
        #       pygame axis system
        #       -----> x
        #       |          A         A = top center
        #       |         / \        x = pos/ship center
        #       V        / x \
        #       y       /     \
        #              /_______\     the triangle represents the ship
        self.pos = start_pos

        # angle

        # angle - rotation angle of the ship, it is 0, when the ship is facing upwards, it is not changed in the Ship
        #         update(), it has to be defined in the update() of the child class before calling the super().update()
        #         function
        self.angle = 0

        # velocity

        # velocity - array carrying the values of the ship speed in both axes [x, y], it is recommended to change this
        #            to move the ship
        self.velocity = np.array([0.0, 0.0])
        # max_velocity - maximum speed of the ship in one axis, in update() the code checks if it is exceeded or not
        self.max_velocity = max_velocity
        # acceleration - acceleration of the ship, it is recommended to use this in movement methode defined in a child
        #                class
        self.acceleration = acceleration
        # velocity_coefficient - used for calculating the position, creates the smooth flow of controlling ships and
        #                        allows better (more detailed) range of speed
        self.velocity_coefficient = velocity_coefficient

        # spawn point

        # sets the ship center at values defined in constructor arguments
        self.rect.center = self.pos

        # attacking

        # dmg - variable containing the ship ram damage
        self.dmg = dmg
        # proj_dmg - variable containing ship projectiles damage
        self.proj_dmg = proj_dmg
        # fire_rate_time - minimal time between firing two projectiles
        self.fire_rate_time = 1 / fire_rate
        # last_shot_time - the time when the last shot was fired, used to decide if a new projectile can be fired or not
        self.last_shot_time = self.time_alive
        # projectile_group - sprite group for storing fired projectiles
        self.projectile_group = projectile_group
        # proj_spawn_offset - offset from a ship center, when the ship is facing upwards, respects pygame axis
        #                     direction, default is set to the top center point
        #                     -----> x
        #                     |                  ---.-------> + proj_spawn_offset[0]
        #                     |                     A
        #                     |                    /.\
        #                     V           |       / . \         A = top center
        #                     y           ......./..x  \        x = ship center
        #                                 |     /       \
        #                                 |    /         \
        #          + proj_spawn_offset[1] V   /___________\     the triangle represents the ship
        #
        self.proj_spawn_offset = np.array([0, - 1/2 * self.height])

        # gun overheating

        # heat - variable containing how much is the ship gun heated
        self.heat = 0
        # overheat - maximum value of heat the gun can withstand, if the heat reaches overheat level, cooling slows down
        #            for a moment, and the ship will not fire
        self.overheat = overheat
        # cooling - how quickly the gun cools down, self.cooling = how much heat the gun looses every frame,
        #           cooling (the constructor's argument) = how much heat the gun looses every second
        self.cooling = cooling/60
        # is_overheated - bool; when true, the gun will not fire, sets True when the heat reaches overheat level, then
        #                 when it cools down to 75% of the overheat level it sets back to False
        self.is_overheated = False
        # overheat_sound - sound which plays when the gun overheats
        self.overheat_sound = pygame.mixer.Sound("assets/sounds/overheat.mp3")
        self.overheat_sound.set_volume(0.55)

        # explosion

        # explosion_size - size of an explosion after the ship is destroyed (see explosion.py for more)
        self.explosion_size = explosion_size

    def update(self) -> None:
        """
        Updates the ship rotation based on the ship angle variables, limits the ship velocity to its maximum value,
        updates the ship position based on the ship velocity and takes care of the gun heat level. It is not recommended
        to change the pos variable directly.
        :return: None
        """

        # rotation
        # It is recommended to change the variable angle before calling the super().update() function!

        # This section rotates the ship's image according to a variable angle. If the angle == 0, then the ship is
        # facing upwards. It also updates the ship's rect and the ship's mask based on the rotated image.
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
        # It is recommended to change the variable velocity before calling the super().update() function!

        # This section calculates the new position of the ship based on its current velocity and velocity coefficient.
        self.pos[0] += self.velocity[0] * self.velocity_coefficient
        self.pos[1] += self.velocity[1] * self.velocity_coefficient
        # This line sets the ship on the newly calculated coordinates.
        self.rect.center = self.pos

        # heat

        # This section cools down the gun (if it's hot or warm)
        if self.heat > 0:
            self.heat -= self.cooling
        else:
            self.heat = 0
        # This section checks if the gun is overheated
        if self.heat >= self.overheat and not self.is_overheated:
            self.is_overheated = True
            self.cooling = 2/3 * self.cooling
            pygame.mixer.find_channel(False).play(self.overheat_sound)
        # This section checks if the gun is cool enough, when it was overheated
        elif self.is_overheated and self.heat < 0.75 * self.overheat:
            self.is_overheated = False
            self.cooling = 3/2 * self.cooling

    @classmethod
    def rot_compute(cls, dist_x: int, dist_y: int) -> float:
        """
        Calculates the angle between two points based on the distances in the x and y axes. Non-absolute values must be
        used for the calculation, otherwise the angle is not calculated correctly. The output of the function is in the
        interval <-90°; 270°). The function gives 0°, when dist_y > 0 and dist_x == 0. Respects normally defined axes
        and positive/negative direction of rotation.
        :param dist_x: Distance in x-axis between two points
        :param dist_y: Distance in y-axis between two points
        :return: Angle between y-axis and hypotenuse between the two points
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

    def shoot(self) -> None:
        """
        If the time after last shot is greater than fire_rate_time and the gun is not overheated, this function creates
        a projectile, adds it to the projectile group and increases the heat level. In the short term: try to fire the
        projectile.
        :return: None
        """
        elapsed_time = self.time_alive - self.last_shot_time
        if elapsed_time >= self.fire_rate_time and not self.is_overheated:
            projectile = Projectile(self)
            self.last_shot_time = self.time_alive
            self.projectile_group.add(projectile)
            self.heat += 1
