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
tree = pygame.image.load("TREE_PNG.png").convert_alpha()


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
    
    def __init__(self, enemies, lands):
        self.enemies = enemies
        self.lands = lands
        self.Enemy_List = []
        self.set_room()            
    
    def set_room(self):
        
        
        for _ in range(self.enemies):
            Enemy_SIZE = 50
            Tree_Size = 50
            Enemy_Buffer = int(Object.Wall_Depth+.5*Enemy_SIZE)
            Obj_Buffer = int(Object.Wall_Depth+.5*Tree_Size)
            if len(Objects)==0:
                New = Object(ghost, (random.randint(Enemy_Buffer, WIDTH-Enemy_Buffer)),\
                random.randint(Enemy_Buffer,HEIGHT-Enemy_Buffer),Enemy_SIZE,True)
                self.Enemy_List.append(New)

            else:
                while True:
                    
                    New = Object(ghost, (random.randint(Enemy_Buffer, WIDTH-Enemy_Buffer)),\
                    random.randint(Enemy_Buffer,HEIGHT-Enemy_Buffer),Enemy_SIZE,True)
                    
                    if New.collide(New.x, New.y)==False:
                        self.Enemy_List.append(New)
                        break
                    else:
                        global Object_Count
                        Object_Count -=1                        
                        Objects.remove(Objects[New.Obj_num])

        for _ in range(self.lands):
            while True:
                    
                New = Object(tree, (random.randint(Obj_Buffer, WIDTH-Obj_Buffer)),\
                random.randint(Obj_Buffer,HEIGHT-Obj_Buffer),Tree_Size)
                
                if New.collide(New.x, New.y)==False:
                    self.Enemy_List.append(New)
                    break
                else:
                    
                    Object_Count -=1                        
                    Objects.remove(Objects[New.Obj_num])
        

# TODO setup the wall class, these are not stored in object list, not checked for collisions,
# They affect the Object.Wall_Depth, so when setting up the level, set enemies outside walls
# Non enemy objects will be added to object list, but not level enemy list

class Wall:
    pass

class Object:
    Wall_Depth = 100
    
    def __init__(self, image, x,y, size,can_move=False):
        self.x = x
        self.y = y
        self.size = size
        self.can_move = can_move 
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
        
        location = find_boundaries(x,y,self.size)        
        
       
        
        for object in Other_Objects:
            # Other object locations
            Loc = find_boundaries(object[0], object[1], object[2])
            if collision(location, Loc)==True:
                return True              
        return False

    def move(self, speed):
        
        if self.direction == None:
            self.direction = self.choices[random.randint(0,len(self.choices)-1)]
        
        Objects[self.Obj_num] = (self.x, self.y, self.size)         

        if self.direction=='R':
            curr = self.x + speed
            # collision with objects
            if self.collide(curr, self.y) == True:
                self.direction = self.choices[random.randint(0,len(self.choices)-1)]
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
                self.direction = self.choices[random.randint(0,len(self.choices)-1)]
                return      

            if curr >0+.5*self.size+Object.Wall_Depth:
                self.x = curr
                self.rect.center = (self.x, self.y)
            else:
                self.direction = 'R'               
                
        elif self.direction == 'U':
            
            curr = self.y - speed
            if self.collide(self.x, curr) == True:
                self.direction = self.choices[random.randint(0,len(self.choices)-1)]
                return      

            if curr >0 + .5*self.size+ Object.Wall_Depth:           
                self.y = curr
                self.rect.center = (self.x, self.y)
            else:
                self.direction = 'D'

        elif self.direction == 'D':
            curr = self.y + speed
            if self.collide(self.x, curr) == True:
                self.direction = self.choices[random.randint(0,len(self.choices)-1)]
                return  

            if curr < HEIGHT- .5*self.size-Object.Wall_Depth:
                self.y = curr
                self.rect.center = (self.x, self.y)
            else:
                self.direction = 'U'

L = Level(20, 20)


while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit() 
    screen.fill(GROUND_COLOR)
    
    for enemy in L.Enemy_List:
        if enemy.can_move==True:
            enemy.move(random.randint(4,6))
        screen.blit(enemy.image, enemy.rect)
        
    pygame.display.flip()