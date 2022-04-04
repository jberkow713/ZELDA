import pygame
import random
import sys
import math
from pygame.locals import(
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_ESCAPE, KEYDOWN, QUIT, K_RETURN
)
# Screen
WIDTH = 1500 #1800
HEIGHT = 1000 #1400
FPS = 60
# Colors
GROUND_COLOR = (255, 222, 179)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (255,0,255)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Legend of Zelda")

ghost = pygame.image.load("ghost.png").convert_alpha()

Object_Count = 0
Objects = []

class Level:
    def __init__(self):
        self.Screen = screen
        

class Object:
    def __init__(self, image, x,y, size):
        self.x = x
        self.y = y
        self.size = size 
        self.image = image
        self.rescale()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.direction = None
        self.choices = ['U','D','L','R']
        self.Obj_num = self.obj_num()
    
    def obj_num(self):
        global Object_Count
        Obj_Num = Object_Count
        Object_Count +=1
        Objects.append((self.x,self.y, self.size))
        return Obj_Num
        

    def rescale(self):
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
    
    def collide(self, x,y):
        '''
        Discovers collisions, returns True if collision exists
        Going to compare x y coords and size to all other items in the object list
        '''
        # This is now a list of all other objects outside of itself
        Other_Objects = Objects.copy()
        Other_Objects.remove(Other_Objects[self.Obj_num])
        print(Other_Objects)
        
        # TODO
        # Take in list of other objects and their x,y coordinates and size, check if current objects coordinates
        # collide with any of the other objects, enemies, etc
        # return True if there is a collision
        pass

    def move(self, speed):
        
        if self.direction == None:
            self.direction = self.choices[random.randint(0,len(self.choices)-1)]
        
        Objects[self.Obj_num] = (self.x, self.y, self.size)         

        if self.direction=='R':
            curr = self.x + speed
            # collision with objects
            if self.collide(curr, self.y) == True:
                self.direction = None
                return  
            # collision with edge of level
            if curr <=WIDTH - .5*self.size: 
                self.x = curr
                self.rect.center = (self.x, self.y)
            else:                
                self.direction = 'L'

        elif self.direction == 'L':
            
            curr = self.x - speed
            if self.collide(curr, self.y) == True:
                self.direction = None
                return      

            if curr >0+.5*self.size:
                self.x = curr
                self.rect.center = (self.x, self.y)
            else:
                self.direction = 'R'               
                
        elif self.direction == 'U':
            
            curr = self.y - speed
            if self.collide(self.x, curr) == True:
                self.direction = None
                return      

            if curr >0 + .5*self.size:           
                self.y = curr
                self.rect.center = (self.x, self.y)
            else:
                self.direction = 'D'

        elif self.direction == 'D':
            curr = self.y + speed
            if self.collide(self.x, curr) == True:
                self.direction = None
                return  

            if curr < HEIGHT- .5*self.size:
                self.y = curr
                self.rect.center = (self.x, self.y)
            else:
                self.direction = 'U'

Level1 = Level()
G = Object(ghost, 700,700,100)
G2 = Object(ghost, 500,500, 100)


while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit() 

    Level1.Screen.fill(GROUND_COLOR)
    
    G2.move(4)    
    G.move(4)
    Level1.Screen.blit(G.image, G.rect)
    Level1.Screen.blit(G2.image, G2.rect)


    pygame.display.flip()



      