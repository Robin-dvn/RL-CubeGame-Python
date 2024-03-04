import pygame
import math2
import engine
import graphics
from jouer import jouer

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_1,
    K_2,
    K_3,
    K_4,
    KEYDOWN,
    QUIT,
)

pygame.init()

screen = pygame.display.set_mode([1000,600])

running = True
player = engine.Player()
background = graphics.Background("ressources/images/background.png")

sprites = pygame.sprite.Group()
sprites.add(player)
map = "ressources/maps/map1.txt"
while running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                print("espace")
                jouer(screen,map)
            elif e.key == K_1:
                print("map1")
                map = "ressources/maps/map1.txt"
            elif e.key == K_2:
                print("map2")
                map = "ressources/maps/map2.txt"
            elif e.key == K_3:
                print("map3")
                map = "ressources/maps/map3.txt"
            elif e.key == K_4:
                print("map4")
                map = "ressources/maps/map4.txt"
                
    
    screen.fill((0,0,0))
    screen.blit(background.surf,background.rect)
    
    
    pygame.display.flip()

pygame.quit()
