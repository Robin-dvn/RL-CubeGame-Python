import pygame
from .tile import caseSol, Pique,PiqueInv, Tile
import math

class Map():
    def __init__(self,src) :
        self.src = src
        self.map = []
        self.nb_lignes = 16
    def charger_map(self):
        fichier = open(self.src,'r')
        tiles = fichier.readlines()
        for tile in tiles:
            self.map.append(int(tile))
    def getPosFromId(self,id):

        return [id/self.nb_lignes,id%self.nb_lignes]


def importer_map(sprites: pygame.sprite.Group, map: Map):
    for i in range(len(map.map)):
        tile = map.map[i]
        pos = map.getPosFromId(i)
        pos[0] = math.trunc(pos[0])
        pos[0] *=25
        pos[1] *= 25
        
        
        if tile == 1:
            newTile = caseSol()
            newTile.rect.topleft = pos[0], pos[1]
            sprites.add(newTile)
        elif tile == 2:
            newTile = Pique()
            newTile.rect.topleft = pos[0], pos[1]
            sprites.add(newTile)
            
        elif tile == 3:
            newTile = PiqueInv()
            newTile.rect.topleft = pos[0], pos[1]
            sprites.add(newTile)


def isValidTile(position):
    if  0<=position[0]<=1000-25:
        if  0<=position[1]<=400-25:
            return True
    return False

def getTileFromPos(position):
    tilex=int(position[0]/25)
    
    tiley=int(position[1]/25)
    
    return tilex * int((400/25))+tiley