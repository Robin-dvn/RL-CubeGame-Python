import pygame
import time
import graphics

class Player(pygame.sprite.Sprite):
    def __init__(self ):
        super().__init__()
        self.surf = pygame.image.load("ressources/images/cube.png").convert_alpha()
        self.image = pygame.image.load("ressources/images/cube.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.surf.get_rect()
        self.inputFlags = InputFlags()
        self.vitesse = [0.,0.]
        self.pos = [75.,300.]
        self.last_time = time.time()
        self.auSol = False
        self.en_saut = False
        self.reward = []
        self.probs = []
        self.action = []
        self.en_jeu = True

    def set_sol(self,ausol):
        self.auSol=ausol

    def au_sol(self,sol):
        if pygame.sprite.spritecollideany(self,sol):
            return True

    def collision_map(self,map_sprite):
        hits=[]
        piques = []
        for tile in map_sprite:
            if type(tile) is graphics.Pique or type(tile) is graphics.PiqueInv:
                piques.append(tile)
            if pygame.sprite.collide_rect(self,tile):
                if  not (type(tile) is graphics.Pique or type(tile) is graphics.PiqueInv):
                    hits.append(tile)
        piques_group = pygame.sprite.Group()
        for pique  in piques:
            piques_group.add(pique)

        if pygame.sprite.spritecollide(self,piques_group,False,pygame.sprite.collide_mask):
            return 1      
        
        return hits

    def apply_col_x(self,map_sprite):
        colisions = self.collision_map(map_sprite)
    
        if colisions == 1:
            self.kill()
            self.en_jeu = False
        else:
            for tile in colisions:
                if self.vitesse[0] >0:
                    self.pos[0] = tile.rect.left -self.rect.w
                    self.rect.x = self.pos[0]
                    self.vitesse[0]=0
                if self.vitesse[0] <0:
                    self.pos[0] = tile.rect.right 
                    self.rect.x = self.pos[0]
                    self.vitesse[0]=0
        #plafond, mur gauche et mur droit
        if self.pos[0] > 1000-25:
            self.pos[0] = 1000-25
            self.vitesse[0] =0
        elif self.pos[0] <0:
            self.pos[0] = 0
            self.vitesse[0] =0
        if self.pos[1] < 0:
            self.pos[1]=0

    def apply_col_y(self,map_sprite,sol):
        if self.au_sol(sol):
            self.auSol =True
            self.en_saut = False
            self.rect.bottomleft = self.rect.x, 400
            self.vitesse[1]=0
            
        else: 
            self.set_sol(False)
            self.en_saut = False

        colisions = self.collision_map(map_sprite)
        
        if colisions == 1:
            self.kill()
            self.en_jeu=False
        else:            
            for tile in colisions:
                if self.vitesse[1] >0:
                    self.auSol = True
                    self.en_saut =False
                    self.pos[1]= tile.rect.top - self.rect.width
                    self.rect.y = self.pos[1]
                if self.vitesse[1] <0:
                    
                    self.pos[1]= tile.rect.top + self.rect.width
                    self.rect.y = self.pos[1]
                    self.vitesse[1]=0
                    
    

        
        #plafond, mur gauche et mur droit
        if self.pos[0] > 1000-25:
            self.pos[0] = 1000-25
            self.vitesse[0] =0
        elif self.pos[0] <0:
            self.pos[0] = 0
            self.vitesse[0] =0
        if self.pos[1] < 0:
            self.pos[1]=0

    def update_pos(self,map_sprite,sol):
        #update position
        current_time = time.time()
        dt = current_time-self.last_time
        
        #horizontal movement   
        if self.inputFlags.right : self.vitesse[0]=220
        if self.inputFlags.left : self.vitesse[0]=-220
        if self.inputFlags.right and not self.auSol and not self.inputFlags.space:
            self.vitesse[0]=75 
        if self.inputFlags.left and not self.auSol and not self.inputFlags.space:
            self.vitesse[0]=-75     
        if self.inputFlags.right and  self.inputFlags.left:
            self.vitesse[0]=0

        
        if  self.vitesse[0]!=0:
            if self.vitesse[0] <0:
                self.vitesse[0] += -20 * self.vitesse[0] *0.02
            else:
                self.vitesse[0] -= 20 * self.vitesse[0] *0.02
            if abs(self.vitesse[0]) < 0.01:
                self.vitesse[0] =0

        self.pos[0] += self.vitesse[0] *dt
        self.rect.x = round(self.pos[0])
        self.apply_col_x(map_sprite)
        #vertical movement   

        if self.inputFlags.up : self.vitesse[1]=-200
        if self.inputFlags.down : self.vitesse[1]=200

        
        if self.inputFlags.space and self.auSol and not self.en_saut : 
            self.vitesse[1]=-380
            self.en_saut = True
            self.auSol = False

        if not self.auSol  or self.en_saut:
            self.vitesse[1]+=887.5 *dt

        self.pos[1] += self.vitesse[1] *dt
        self.rect.y = round(self.pos[1])

        self.apply_col_y(map_sprite,sol)
        self.last_time = current_time

    def get_state(self,map : graphics.Map):
        state = []
        state.append(0)
        state.append(int(self.pos[0]/25))
        state.append(int(self.pos[1]/25))
        state.append(self.vitesse[0])
        state.append(self.vitesse[1])

        for i in range(-3,4):
            for j in range(-3,4):
                if not (j==0 and i==0):
                    pos_tile=[self.pos[0]+25*i,self.pos[1]+25*j]
                    if not graphics.isValidTile(pos_tile):

                        if pos_tile[0] <self.pos[0]:

                            pos_int = [self.pos[0] +25*i,self.pos[1]]
                            if not graphics.isValidTile(pos_int):
                                state.append(-1)
                            else:
                                if pos_tile[1] < self.pos[1]:
                                    state.append(-3)
                                else : state.append(-4)
                        else:

                            pos_int = [self.pos[0] +25*i,self.pos[1]]
                            if not graphics.isValidTile(pos_int):
                                state.append(-2)
                            else:
                                if pos_tile[1] < self.pos[1]:
                                    state.append(-3)
                                else : state.append(-4)
                    else:
                        #si la position de la tile est valide:
                        tile = graphics.getTileFromPos(pos_tile)
                        state.append(map.map[tile])
        
        return state

    def reset(self):
        self.inputFlags = InputFlags()
        self.vitesse = [0.,0.]
        self.pos = [50.,300.]
        self.last_time = time.time()
        self.auSol = False
        self.en_saut = False
        self.reward = []
        self.probs = []
        self.action = []
        self.en_jeu = True

    def getReward(self):
        if self.en_jeu:
            self.reward.append(0)
            
        else:
            self.reward.append( self.pos[0])
            
    def canReward(self):
        
        for reward in self.reward:
            if reward != 0:
                return False
        return True







class InputFlags():
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.space = False
    def print_obj(self):
        print(f"[{self.right},{self.left},{self.up},{self.down},{self.space}]")
    def reset(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.space = False

