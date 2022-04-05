from re import L
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

def find_boundaries(x,y, size):
    x_bounds = int(x -.5*size), int(x + .5*size)
    y_bounds = int(y-.5*size), int(y+.5*size)

    return x_bounds, y_bounds

def collision(a,b):
    
    in_between = False
    if a[0][0] >=b[0][0] and a[0][0]<= b[0][1]:
        in_between=True
    if a[0][1]>=b[0][0] and a[0][1]<=b[0][1]:
        in_between=True    

    if in_between == True:
        if a[1][0] >=b[1][0] and a[1][0] <=b[1][1]:
            return True
        if a[1][1] >=b[1][0] and a[1][1] <=b[1][1]:
            return True   

class Level:
    def __init__(self, enemies, starting_x):
        self.enemies = enemies
        self.starting_x = starting_x
        self.Enemy_List = []
        self.set_landscape()
        self.set_enemies()        
    
    def set_landscape(self):
        pass

    def set_enemies(self):
        
        for _ in range(self.enemies):
            self.Enemy_List.append(Object(ghost, (self.starting_x),random.randint(175,HEIGHT-175),100, True))
            self.starting_x += WIDTH/self.enemies-Object.Wall_Depth/self.enemies    

class Object:
    Wall_Depth = 100
    
    def __init__(self, image, x,y, size, movable):
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
        self.movable = movable
    
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
        
        location = find_boundaries(x,y,self.size)        
        
        for object in Other_Objects:
            # Other object locations
            Loc = find_boundaries(object[0], object[1], object[2])
            if collision(location, Loc)==True:
                return True              

    def move(self, speed):
        
        if self.direction == None:
            self.direction = self.choices[random.randint(0,len(self.choices)-1)]
        
        Objects[self.Obj_num] = (self.x, self.y, self.size)         

        if self.direction=='R':
            curr = self.x + speed
            # collision with objects
            if self.collide(curr, self.y) == True:
                self.direction = 'L'
                return  
            # collision with edge of level
            if curr <=WIDTH - .5*self.size-Object.Wall_Depth: 
                self.x = curr
                self.rect.center = (self.x, self.y)
            else:                
                self.direction = 'L'

        elif self.direction == 'L':
            
            curr = self.x - speed
            if self.collide(curr, self.y) == True:
                self.direction = 'R'
                return      

            if curr >0+.5*self.size+Object.Wall_Depth:
                self.x = curr
                self.rect.center = (self.x, self.y)
            else:
                self.direction = 'R'               
                
        elif self.direction == 'U':
            
            curr = self.y - speed
            if self.collide(self.x, curr) == True:
                self.direction = 'D'
                return      

            if curr >0 + .5*self.size+ Object.Wall_Depth:           
                self.y = curr
                self.rect.center = (self.x, self.y)
            else:
                self.direction = 'D'

        elif self.direction == 'D':
            curr = self.y + speed
            if self.collide(self.x, curr) == True:
                self.direction = 'U'
                return  

            if curr < HEIGHT- .5*self.size-Object.Wall_Depth:
                self.y = curr
                self.rect.center = (self.x, self.y)
            else:
                self.direction = 'U'

L = Level(5, 175)

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit() 
    screen.fill(GROUND_COLOR)

    for enemy in L.Enemy_List:
        if enemy.movable == True:
            
            enemy.move(random.randint(4,6))
            screen.blit(enemy.image, enemy.rect)
        
    pygame.display.flip()