import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, src):
        super().__init__()
        self.surf = pygame.image.load(src).convert()
        self.rect = self.surf.get_rect()