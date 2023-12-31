import pygame.sprite

class Projectile_collision(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.sound = pygame.mixer.Sound("assets/sounds/video_game_hit_sound.mp3")  # Load sound file
        self.sound.set_volume(0.05)
        self.sound.play()
        for num in range(1, 8):
            img = pygame.image.load(f"assets/animations/projectile_collision1/proj_col{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (150, 150))
            if size == 2:
                img = pygame.transform.scale(img, (300, 300))
            if size == 3:
                img = pygame.transform.scale(img, (500, 500))
            # add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.counter = 0


    def update(self):
        explosion_speed = 2
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()