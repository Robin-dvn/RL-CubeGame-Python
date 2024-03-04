import pygame
from .player import Player
import graphics
import time



class Env():
    def __init__(self, nb_players: int, map_chem :str,screen:pygame.Surface):
        self.screen =screen
        self.players = pygame.sprite.Group()
        self.playerRFL =[]
        for i in range(nb_players):
            player = Player()
            self.players.add(player)
            self.playerRFL.append(player)
        self.fond = graphics.Background("ressources/images/fond.png")
        self.sol = graphics.Sol("ressources/images/sol.png")
        self.map = graphics.Map(map_chem)
        self.map.charger_map()
        self.start = time.time()
        self.time = 10000

        self.map_sprites = pygame.sprite.Group()
        graphics.importer_map(self.map_sprites,self.map)
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.fond)
        self.sprites.add(self.sol)
        graphics.importer_map(self.sprites,self.map)
        for player in self.players:
            self.sprites.add(player)
        self.groupe_sol = pygame.sprite.Group()
        self.groupe_sol.add(self.sol)
        self.font = pygame.font.Font("ressources/fonts/Roboto-Medium.ttf",32)


    def step(self,actions):
        for action,player in zip(actions,self.players):
            player:Player
            player.inputFlags.reset()
            if action == 1:
                player.inputFlags.left= True
            elif action == 2:
                player.inputFlags.right= True
            elif action == 3:
                #player.inputFlags.space= True
                pass
            elif action == 4:
                #player.inputFlags.space= True
                player.inputFlags.right= True
            elif action == 5:
                #player.inputFlags.space= True
                player.inputFlags.left= True
            player.update_pos(self.map_sprites,self.groupe_sol)
            if self.time<0:
                player.kill()
                player.en_jeu=False
            player.action.append(action)
        for entity in self.sprites:
            self.screen.blit(entity.surf,entity.rect)

        text = self.font.render(f"temps restant {int(self.time/1000)+1}",True,(255,255,255),None)
        text_rect = text.get_rect()
        text_rect.center=(500,500)
        self.screen.blit(text,text_rect)
        pygame.display.flip()

        states = []
       
        for player in self.players:
            states.append(player.get_state(self.map))
        for player in self.playerRFL:
            if player.canReward():
               player.getReward()
       
        temp_ecoule = time.time()- self.start
        self.time = 10000-temp_ecoule*1000



        return states

    def best_player(self):
        max= -20000
        best :Player
        
        for player in self.playerRFL:
            
            player : Player
            if player.reward[-1] > max:
                max = player.reward[-1] 
                best = player
        return best
    
    def reset(self):
        
        for player in self.players:
            player.kill()
        for i in self.playerRFL:
            player = Player()
            self.players.add(player)
        self.playerRFL =[]
        for player in self.players:
            self.playerRFL.append(player)
            self.sprites.add(player)
        self.start = time.time()
        self.time = 10000
        
        states= []
        for player in self.playerRFL:
            player : Player
            states.append(player.get_state(self.map))

        return states

        
     

        
        
    