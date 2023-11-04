import pygame


class Crosshair(pygame.sprite.Sprite):
    # This class is for crosshair. By calling the constructor it makes mouse invisible and creates crosshair on its
    # position. By calling the update() function it reads position of the mouse and moves the image of crosshair to the
    # mouse's location. While updating sprite groups, update the crosshair one as the last one, to make it visible on
    # top of other sprites.
    def __init__(self, picture_path):
        super().__init__()
        pygame.mouse.set_visible(False)
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
