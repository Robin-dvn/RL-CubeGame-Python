import pygame 

class Tile(pygame.sprite.Sprite):
    def __init__(self) :
        super().__init__()
        
class caseSol(Tile):
    def __init__(self) :
        super().__init__()
        self.surf = pygame.image.load("ressources/images/solide1.png").convert_alpha()
        self.rect = self.rect = self.surf.get_rect()
class Pique(Tile):
    def __init__(self) :
        super().__init__()
        self.surf = pygame.image.load("ressources/images/pique.png").convert_alpha()
        self.image = pygame.image.load("ressources/images/pique.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect = self.surf.get_rect()
class PiqueInv(Tile):
    def __init__(self) :
        super().__init__()
        self.surf = pygame.image.load("ressources/images/pique_inverse.png").convert_alpha()
        self.image = pygame.image.load("ressources/images/pique_inverse.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect = self.surf.get_rect()