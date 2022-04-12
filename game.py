from re import L
from tkinter import W
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

link_down = pygame.image.load("Link.png").convert_alpha()
link_up = pygame.image.load("Link_Up_Advanced.jpg").convert_alpha()
link_left = pygame.image.load("Link_Left_advanced.png").convert_alpha()
link_right = pygame.image.load("Link_Right_Advanced.png").convert_alpha()

sword_down = pygame.image.load("Link_Sword_Down.png").convert_alpha()
sword_up = pygame.image.load("Link_Sword_Up.jpg").convert_alpha()
sword_left = pygame.image.load("Link_Sword_Left.jpg").convert_alpha()
sword_right = pygame.image.load("Link_Sword_Right.png").convert_alpha()

ghost = pygame.image.load("ghost.png").convert_alpha()
tree = pygame.image.load("TREE_PNG.png").convert_alpha()
wall = pygame.image.load("Zelda_Wall.jpg").convert_alpha()

Link_Placement = None
Sword_Placement = None
Sword_Direction = None
Object_Count = 0
Objects = []
Projectiles = []

def attack_distance(x,y):
    
    Link_X = Objects[Link_Placement][0]
    Link_Y = Objects[Link_Placement][1]

    return  math.sqrt(abs(Link_X-x)**2 +abs(Link_Y-y)**2)

def find_boundaries(x,y, size):
    x_bounds = int(x -.5*size), int(x + .5*size)
    y_bounds = int(y-.5*size), int(y+.5*size)

    return x_bounds, y_bounds

def pushback(x,y, direction, distance):
    if direction == 'U':
        return x, y-distance
    elif direction =='D':
        return x,y+distance
    elif direction == 'L':
        return x-distance,y
    elif direction == 'R':
        return x+distance,y

def off_walls(x,y,size):
    if x <= WIDTH - .5*size-Wall.Wall_Depth and x>0+.5*size+Wall.Wall_Depth:
        if y >0 + .5*size+ Wall.Wall_Depth and y < HEIGHT- .5*size-Wall.Wall_Depth:
            return True                 

def choose_new_path(LIST, LST2):
    l = LIST.copy()
    for val in LST2:
        l.remove(val)
    return l[random.randint(0,len(l)-1)]

def collision(a,b):
    
    in_between = False
    if a[0][0] >=b[0][0] and a[0][0]<= b[0][1]:
        in_between=True
    if a[0][1]>=b[0][0] and a[0][1]<=b[0][1]:
        in_between=True
    if b[0][0] >=a[0][0] and b[0][0]<= a[0][1]:
        in_between=True
    if b[0][1]>=a[0][0] and b[0][1]<=a[0][1]:
        in_between=True    

    if in_between == True:
        if a[1][0] >=b[1][0] and a[1][0] <=b[1][1]:
            return True
        if a[1][1] >=b[1][0] and a[1][1] <=b[1][1]:
            return True
        if b[1][0] >=a[1][0] and b[1][0] <=a[1][1]:
            return True
        if b[1][1] >=a[1][0] and b[1][1] <=a[1][1]:
            return True
class Sword:
    SIZE = 75
    def __init__(self,owner):
        self.owner = owner
        self.x = -1000
        self.y = -1000
        self.size = Sword.SIZE
        self.obj_num = self.obj_num()
        self.direction = None 

    def obj_num(self):
        global Object_Count
        global Sword_Placement
        Sword_Placement =Obj_Num = Object_Count 
        Object_Count +=1
        Objects.append((self.x,self.y, self.size))
        return Obj_Num               

    def rescale(self):
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)    
    
    def load_sword(self):
        global Sword_Direction
        if self.owner.direction=='U':
            Sword_Direction = self.direction = 'U'
            self.image = sword_up
            self.x = self.owner.x
            self.y = self.owner.y - .75*self.owner.size
            self.rescale()
            return self.image
        if self.owner.direction=='D':
            Sword_Direction = self.direction = 'D'
            self.image = sword_down
            self.x = self.owner.x
            self.y = self.owner.y + .6*self.owner.size
            self.rescale()
            return self.image    
        if self.owner.direction=='R':
            Sword_Direction = self.direction = 'R'
            self.image = sword_right
            self.x = self.owner.x+.6*self.owner.size
            self.y = self.owner.y 
            self.rescale()
            return self.image    
        if self.owner.direction=='L':
            Sword_Direction  = self.direction = 'L'
            self.image = sword_left
            self.x = self.owner.x-.6*self.owner.size
            self.y = self.owner.y 
            self.rescale()
            return self.image
class Link:
    def __init__(self, image, x, y, size,speed):
        self.image = image
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.rescale()
        self.direction = 'D'
        self.can_move = True
        self.Obj_num = self.obj_num()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.sword = Sword(self)

    def obj_num(self):
        global Object_Count
        global Link_Placement
        Link_Placement = Obj_Num = Object_Count
        Object_Count +=1
        Objects.append((self.x,self.y, self.size, self.can_move))
        return Obj_Num        
    
    def find_image(self):
                
        if self.direction == 'D':
            self.image = link_down
        elif self.direction == 'U':
            self.image = link_up
        elif self.direction == 'R':
            self.image = link_right
        elif self.direction == 'L':
            self.image = link_left
        self.rescale()                
        
    def rescale(self):
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
    
    def collide(self, x,y):
        '''
        Discovers collisions, returns True if collision exists
        Going to compare x y coords and size to all other items in the object list
        '''
        # This is now a list of all other objects outside of itself
        Other_Objects = Objects.copy()
        # Removing Link and Sword from Object list to avoid colliding with self
        Other_Objects.remove(Other_Objects[0])
        Other_Objects.remove(Other_Objects[0])            
            
        location = find_boundaries(x,y,self.size)      
        
        for object in Other_Objects:
            # Other object locations
            Loc = find_boundaries(object[0], object[1], object[2])
            if collision(location, Loc)==True:
                return True              
            
    def move(self):
        keys = pygame.key.get_pressed()
        
        Objects[self.Obj_num] = (self.x, self.y, self.size, self.can_move)

        if keys[pygame.K_RETURN]:
            self.sword.load_sword()
            Objects[Sword_Placement] = (self.sword.x, self.sword.y, self.sword.size)
            return

        if keys[pygame.K_UP] and not keys[pygame.K_DOWN] \
            and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:

            curr = self.y - self.speed
            if self.collide(self.x, curr) == True:
                return      

            if curr >0 + .5*self.size+ Wall.Wall_Depth:           
                self.y = curr
                self.rect.center = (self.x, self.y)
                self.direction = 'U'
        
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP]\
            and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:

            curr = self.y + self.speed
            if self.collide(self.x, curr) == True:
                return      

            if curr <HEIGHT- .5*self.size- Wall.Wall_Depth:           
                self.y = curr
                self.rect.center = (self.x, self.y)
                self.direction = 'D'
        
        if keys[pygame.K_RIGHT] and not keys[pygame.K_UP]\
            and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT]:

            curr = self.x + self.speed
            if self.collide(curr, self.y)==True:
                return

            if curr <WIDTH - .5*self.size -Wall.Wall_Depth:
                self.x = curr
                self.rect.center = (self.x, self.y)
                self.direction = 'R' 
        
        if keys[pygame.K_LEFT] and not keys[pygame.K_UP]\
            and not keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]:

            curr = self.x - self.speed
            if self.collide(curr,self.y)==True:
                return

            if curr >0 + .5*self.size +Wall.Wall_Depth:
                self.x = curr
                self.rect.center = (self.x, self.y)
                self.direction = 'L'          
                 
class Level:
    
    def __init__(self, enemies, lands,enemy_size, land_size, enemy_speed):
        self.enemies = enemies
        self.lands = lands
        self.enemy_size = enemy_size
        self.land_size = land_size
        self.enemy_speed = enemy_speed
        self.Object_List = []
        self.Wall_List = []
        self.set_room()            
    
    def set_room(self):        
        # Enemies               

        for _ in range(self.enemies):
            Enemy_SIZE = self.enemy_size
            Tree_Size = self.land_size
            Enemy_Buffer = int(Wall.Wall_Depth+.5*Enemy_SIZE)
            Obj_Buffer = int(Wall.Wall_Depth+.5*Tree_Size)
            if len(Objects)==0:
                New = Object(ghost, (random.randint(Enemy_Buffer, WIDTH-Enemy_Buffer)),\
                random.randint(Enemy_Buffer,HEIGHT-Enemy_Buffer),Enemy_SIZE,self.enemy_speed,True)
                self.Object_List.append(New)

            else:
                while True:                    
                    New = Object(ghost, (random.randint(Enemy_Buffer, WIDTH-Enemy_Buffer)),\
                    random.randint(Enemy_Buffer,HEIGHT-Enemy_Buffer),Enemy_SIZE,self.enemy_speed,True)
                    
                    if New.collide(New.x, New.y)==False:
                        self.Object_List.append(New)
                        break
                    else:
                        global Object_Count
                        Object_Count -=1                        
                        Objects.remove(Objects[New.Obj_num])
        # Land Objects
        for _ in range(self.lands):
            while True:
                    
                New = Object(tree, (random.randint(Obj_Buffer, WIDTH-Obj_Buffer)),\
                random.randint(Obj_Buffer,HEIGHT-Obj_Buffer),Tree_Size,0)
                
                if New.collide(New.x, New.y)==False:
                    self.Object_List.append(New)
                    break
                else:                    
                    Object_Count -=1                        
                    Objects.remove(Objects[New.Obj_num])
        # Walls
        Wall_Size = Wall.Wall_Depth*2
        for i in range((WIDTH//Wall_Size)+1):
            self.Wall_List.append(Wall(wall, i*Wall_Size, 0, Wall_Size))
            self.Wall_List.append(Wall(wall, i*Wall_Size, HEIGHT,Wall_Size ))
        for i in range((HEIGHT//Wall_Size)+1):
            self.Wall_List.append(Wall(wall, 0, i*Wall_Size, Wall_Size))
            self.Wall_List.append(Wall(wall, WIDTH, i*Wall_Size, Wall_Size))

class Wall:

    Wall_Depth = 100
    
    def __init__(self, image, x,y,size):
        self.image = image
        self.x = x
        self.y = y
        self.size = size
        self.rescale()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def rescale(self):
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

class Object:    
    
    def __init__(self, image, x,y, size,speed,can_move=False):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.can_move = can_move 
        self.image = image
        self.rescale()
        self.can_move = can_move
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.direction = None
        self.choices = ['U','D','L','R']
        self.Obj_num = self.obj_num()
        self.distance_dict = {}
        self.attacking = False
        self.health =random.randint(15,20)
        self.attack_distance = 400
        self.dead = False
        self.Obj_Collision = False
        self.forced_move = False
        self.forced_direction = None
        self.forced_counter = 0
        
                               
    
    def obj_num(self):
        global Object_Count
        Obj_Num = Object_Count
        Object_Count +=1
        Objects.append((self.x,self.y, self.size, self.can_move))
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
        # First checking for sword collision
        Sword = Objects[Sword_Placement]
        
        Sword_Loc = find_boundaries(Sword[0],Sword[1],Sword[2])
        if collision(location, Sword_Loc) == True:
            self.health -=1            
            return 'Hit'
        # Collision for other objects
        for object in Other_Objects:
                        
            # Other object locations
            Loc = find_boundaries(object[0], object[1], object[2])
            if collision(location, Loc)==True:
                if object[3]==False:
                    self.Obj_Collision = True
                    return True

                self.Obj_Collision=False
                return True        
        
        
        return False   
    
    #TODO Create enemy projectile firing
    def shoot_projectile(self):
        # If enemy within certain x range and y range lines up, or certain y range and x range lines up, 
        # Based on the enemy direction, projectile will be shot at Link, it will go until off screen, needs to be 
        # tracked until off screen, then removed from list,
        # each projectile stored in Global List, once fired, will track to see if it hits link, 
        # will track to see if it's off screen, and once it is, it will be removed from the global list
        pass
    def choose_dir(self, dirs):
        x = Objects[Link_Placement][0]
        y = Objects[Link_Placement][1]

        if dirs == 'U':
            Down = abs((self.y +1)-y) 
            Up = abs((self.y -1) - y)
            if Down < Up:
                return 'D'
            else:
                return 'U'

        if dirs == 'R':
            Right = abs((self.x +1)-x) 
            Left = abs((self.x -1) - x)
            if Right < Left:
                return 'R'
            else:
                return 'L'



    def create_attack(self):
        
        for Dir in self.choices:
            if Dir == 'U':
                y = self.y - self.speed
                if self.collide(self.x, y) ==False:
                    self.distance_dict[Dir] = attack_distance(self.x,y)
                else:
                    self.distance_dict[Dir] = 1000

            if Dir == 'D':
                y = self.y + self.speed
                if self.collide(self.x, y) ==False:
                    self.distance_dict[Dir] = attack_distance(self.x,y)
                else:
                    self.distance_dict[Dir] = 1000

            if Dir == 'L':
                x = self.x - self.speed
                if self.collide(x, self.y ) ==False:
                    self.distance_dict[Dir] = attack_distance(x,self.y)
                else:
                    self.distance_dict[Dir] = 1000

            if Dir == 'R':
                x = self.x + self.speed
                if self.collide(x, self.y) ==False:
                    self.distance_dict[Dir] = attack_distance(x,self.y)
                else:
                    self.distance_dict[Dir] = 1000
                     
        if min(self.distance_dict.values())>self.attack_distance:
            self.attacking = False            
            return 

        else:
            self.direction = min(self.distance_dict, key=self.distance_dict.get)
            self.attacking = True
            return             
        
    def move(self):

        random_dir = self.choices[random.randint(0,len(self.choices)-1)]    
        if self.direction == None:            
            self.direction = random_dir
               
        
        if self.forced_move ==False:
            self.create_attack()
        
        if self.forced_move == True:
            self.direction = self.forced_direction
            self.forced_counter +=1
        if self.forced_counter ==45:
            self.forced_move = False
            self.forced_counter = 0 

            
        Objects[self.Obj_num] = (self.x, self.y, self.size, self.can_move)         
        
        if self.direction=='R':
            curr = self.x + self.speed            
            C = self.collide(curr+self.speed, self.y)
            
            if self.forced_move == False:

                if C == True:

                    if self.attacking == True:
                        if self.Obj_Collision == True:

                            self.direction = self.choose_dir('U')
                            # TODO create function here that evaluates moving both directions, and takes one
                            # That moves enemy closer to link
                            self.forced_direction = self.direction
                            self.forced_move = True
                        return 
                                            
                    self.direction = random_dir
                    return            
                                

            elif C == 'Hit':
                                
                new_x, new_y =  pushback(curr,self.y, Sword_Direction,100)
                if self.collide(new_x, new_y) == True:                    
                    return  
                if off_walls(new_x,new_y, self.size)==True:
                    self.x = new_x
                    self.y = new_y
                    self.rect.center = (self.x, self.y)
                    return 
                else:
                    return  
            # collision with edge of level
            
            if curr <=WIDTH - .5*self.size-Wall.Wall_Depth: 
                self.x = curr
                self.rect.center = (self.x, self.y)
                
                self.direction=='R'

            else:
                self.direction = random_dir
                

        elif self.direction == 'L':            
            curr = self.x - self.speed            
            C = self.collide(curr-self.speed, self.y)
            if self.forced_move == False:            
                if C == True:
                    if self.attacking == True:
                        if self.Obj_Collision == True:

                            self.direction = self.choose_dir('U')
                            self.forced_direction = self.direction
                            self.forced_move = True
                            return 
                                                    
                    self.direction = random_dir
                    return     

            elif C == 'Hit':
                                
                new_x, new_y =  pushback(curr,self.y, Sword_Direction,100)
                if self.collide(new_x, new_y) == True:
                    return  
                if off_walls(new_x,new_y, self.size)==True:
                    self.x = new_x
                    self.y = new_y
                    self.rect.center = (self.x, self.y)
                    return 
                else:
                    return      

            if curr >0+.5*self.size+Wall.Wall_Depth:
                self.x = curr
                self.rect.center = (self.x, self.y)
                
                self.direction = 'L'
               
            else:
                self.direction = random_dir
                             
                
        elif self.direction == 'U':
            
            curr = self.y - self.speed            
            C = self.collide(self.x, curr-self.speed)
            if self.forced_move == False:            
                if C == True:
                    if self.attacking == True:
                        if self.Obj_Collision == True:

                            self.direction = self.choose_dir('R')
                            self.forced_direction = self.direction
                            self.forced_move = True
                            return                               
                    
                    self.direction = random_dir
                    return     

            elif C == 'Hit':                                
                new_x, new_y =  pushback(self.x,curr, Sword_Direction,100)
                if self.collide(new_x, new_y) == True:
                    return  
                if off_walls(new_x,new_y, self.size)==True:
                    self.x = new_x
                    self.y = new_y
                    self.rect.center = (self.x, self.y)
                    return 
                else:
                    return      

            if curr >0 + .5*self.size+ Wall.Wall_Depth:           
                self.y = curr
                self.rect.center = (self.x, self.y)

                self.direction == 'U'                
                
            else:
                self.direction = random_dir
                

        elif self.direction == 'D':
            curr = self.y + self.speed            
            C = self.collide(self.x, curr+self.speed)
            if self.forced_move == False:            
                if C == True: 
                    if self.attacking == True:
                        if self.Obj_Collision == True:

                            self.direction = self.choose_dir('R')
                            self.forced_direction = self.direction
                            self.forced_move = True
                            return                   
                
                    self.direction = random_dir
                    return     

            elif C == 'Hit':                                
                new_x, new_y =  pushback(self.x,curr, Sword_Direction,100)
                if self.collide(new_x, new_y) == True:
                    return  
                if off_walls(new_x,new_y, self.size)==True:
                    self.x = new_x
                    self.y = new_y
                    self.rect.center = (self.x, self.y)
                    return 
                else:
                    return  

            if curr < HEIGHT- .5*self.size-Wall.Wall_Depth:
                self.y = curr
                self.rect.center = (self.x, self.y)

                self.direction = 'D'
                
            else:
                self.direction = random_dir
                
Dead = 0
E = 0

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit() 
    screen.fill(WHITE)
    
    # To Start Level
    if Dead == E:
        print('New Level')
        Level_Reset = True        
        
    if Level_Reset == True:
        E = 0
        Objects.clear()
        Object_Count = 0
        Player = Link(link_down,500,500,75,10)
        L = Level(1,4,75,50,3)
        E += L.enemies
        Level_Reset = False               
           
    for WaLL in L.Wall_List:
        screen.blit(WaLL.image, WaLL.rect)
    
    Objects[Sword_Placement] = (-1000,-1000,Sword.SIZE) 
    Player.move()   
    
    Dead = 0 
    for enemy in L.Object_List:
        if enemy.can_move==True:
            
            if enemy.health >0:
                enemy.move()            
                
                screen.blit(enemy.image, enemy.rect)
            elif enemy.health <=0:
                Objects[enemy.Obj_num]= (-1000,-1000,0)
                enemy.dead = True
                Dead +=1    
        else:
            screen.blit(enemy.image, enemy.rect)
    
    Player.find_image()
    screen.blit(Player.image, Player.rect)

    if Objects[Sword_Placement][0]!=-1000:
        
        screen.blit(Player.sword.image, Player.sword.rect)    
        
    pygame.display.flip()