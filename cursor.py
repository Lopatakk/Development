import pygame
from screensetup import ScreenSetup


class Cursor(pygame.sprite.Sprite):
    """
    This is class for crosshair.
    By calling the constructor it makes mouse invisible and creates crosshair on its position. It also uses the
    convert_alpha function to improve performance.
    By calling the update() function it reads position of the mouse and moves the image of crosshair to the mouse's
    location. While updating sprite groups, update the crosshair one as the last one, to make it visible on top of
    other sprites.
    The disable() function makes the mouse visible again and destroys the sprite, so it does not have to make updates
    when not needed. If you want to switch back to crosshair, you have to create a new one by calling the constructor.
    """
    def __init__(self):
        super().__init__()
        # cursor
        self.cursor_image = pygame.image.load("assets/images/cursor.png")
        self.cursor_image = pygame.transform.scale(self.cursor_image, (0.015 * ScreenSetup.width, 0.015 * ScreenSetup.width))
        self.cursor_image = pygame.Surface.convert_alpha(self.cursor_image)
        # crosshair
        self.crosshair_image = pygame.image.load("assets/images/crosshair.png")
        self.crosshair_image = pygame.Surface.convert_alpha(self.crosshair_image)
        # setting up
        pygame.mouse.set_visible(False)
        self.image = self.cursor_image
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def set_cursor(self):
        self.image = self.cursor_image

    def set_crosshair(self):
        self.image = self.crosshair_image

    def destroy(self):
        pygame.mouse.set_visible(True)
        self.kill()
