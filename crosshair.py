import pygame


class Crosshair(pygame.sprite.Sprite):
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
        pygame.mouse.set_visible(False)
        self.image = pygame.image.load("assets/images/crosshair.png")
        self.image = pygame.Surface.convert_alpha(self.image)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def disable(self):
        pygame.mouse.set_visible(True)
        self.kill()

    def destroy(self):
        self.kill()

