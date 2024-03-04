import pygame
import time
import math
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    KEYUP,
    QUIT,
)
import engine
import graphics
import math2

def jouer( screen : pygame.Surface,map : str ):


    auto = False

    if auto :
        env = engine.Env(10,map,screen)

        actions = []
        probs = []
        agent = engine.REINFORCE()

        
        clock = pygame.time.Clock()

        
        

        for i in range(100):
            states=env.reset()
            en_jeu = True

            while en_jeu:            
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        en_jeu = False

                for i in range(len(env.players)):

                    action, prob = agent.sample_action(states[i])
                
                    actions.append(action[0])
                    probs.append(prob)
                
                
                states= env.step(actions)
                #mettre les trucs de chaque player
                compteur = 0
                
                for player in env.playerRFL:

                    player :engine.Player
                    if player.en_jeu:
                        
                        player.probs.append(probs[compteur])
                        compteur+=1
                    
                

                
                
                actions=[]
                probs=[]

                if len(env.players)==0:
                    en_jeu=False
                
                
                clock.tick(60)
            #trouver le meilleur player
            best = env.best_player()
            #faire l'update par rapport à ce player
            agent.update(best)

            
            


    else:

        player = engine.Player()
        fond = graphics.Background("ressources/images/fond.png")
        sol = graphics.Sol("ressources/images/sol.png")
        map = graphics.Map(map)
        map.charger_map()

        map_sprites = pygame.sprite.Group()
        graphics.importer_map(map_sprites,map)
        sprites = pygame.sprite.Group()
        sprites.add(fond)
        sprites.add(sol)
        graphics.importer_map(sprites,map)
        sprites.add(player)

        group_sol = pygame.sprite.Group()
        group_sol.add(sol)


        en_jeu = True
        clock = pygame.time.Clock()
        previous_time = time.time()
        while en_jeu:
            dt = time.time()- previous_time
            previous_time = time.time()
            player.dt =dt
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    en_jeu = False
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        player.inputFlags.down = True
                    elif event.key == K_UP:
                        player.inputFlags.up = True
                    elif event.key == K_RIGHT:
                        player.inputFlags.right = True
                    elif event.key == K_LEFT:
                        player.inputFlags.left = True
                    elif event.key == K_SPACE:
                        player.inputFlags.space = True
                if event.type == KEYUP:
                    if event.key == K_DOWN:
                        player.inputFlags.down = False
                    elif event.key == K_UP:
                        player.inputFlags.up = False
                    elif event.key == K_RIGHT:
                        player.inputFlags.right = False
                    elif event.key == K_LEFT:
                        player.inputFlags.left = False
                    elif event.key == K_SPACE:
                        player.inputFlags.space = False

            player.update_pos(map_sprites,group_sol)
            for entity in sprites:
                screen.blit(entity.surf,entity.rect)
            pygame.display.flip()
            end = pygame.time.get_ticks()
            
            clock.tick(60)
        

    


        
        