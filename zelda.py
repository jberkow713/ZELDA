import pygame
import random
from sys import exit
from pygame.locals import  *
import copy
import math 
pygame.init()

WIDTH=1400
HEIGHT=1000

BG_Color = (255, 222, 179)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font('font.ttf',50)
pygame.display.set_caption('Zelda')
clock = pygame.time.Clock()

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
heart = pygame.image.load("Heart.png").convert_alpha()
weapon = pygame.image.load("Enemy_Weapon.jpg").convert_alpha()
Enemies = pygame.sprite.Group()

class Sword:
    def __init__(self,x,y,image):
        self.x = x
        self.y = y 
        self.size = 75
        self.image = image 
        self.rescale()
        self.rect = self.image.get_rect(bottomleft=(self.x,self.y))
    def rescale(self):
        self.image = pygame.transform.scale(self.image, (self.size,self.size)) 
    def blit(self):
        screen.blit(self.image,self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.size = 75 
        self.image = link_down
        self.rescale()
        self.rect = self.image.get_rect(bottomleft=(self.x,self.y))
        self.speed = 5
        self.health = 100
        self.dir = None    
    
    def rescale(self):
        self.image = pygame.transform.scale(self.image, (self.size,self.size))

    def blit(self):
        screen.blit(self.image,self.rect)
    def sword_coords(self):
        if self.dir == None:
            return 
        if self.dir == 'r':
            return self.rect.x + self.size, self.rect.y+self.size,sword_right 
        if self.dir == 'l':
            return self.rect.x - self.size, self.rect.y+self.size,sword_left
        if self.dir == 'u':
            return self.rect.x, self.rect.y,sword_up
        if self.dir == 'd':
            return self.rect.x, self.rect.y+2*self.size,sword_down     
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.rect.x + self.speed <= WIDTH - self.size:
                self.image = link_right
                self.rescale()
                self.rect.x +=self.speed
                self.dir = 'r'                
        if keys[pygame.K_LEFT]:
            if self.rect.x - self.speed >0:
                self.image = link_left
                self.rescale()
                self.rect.x -=self.speed
                self.dir = 'l'
        if keys[pygame.K_UP]:
            if self.rect.y - self.speed > 0:
                self.image = link_up
                self.rescale()
                self.rect.y =self.rect.y - self.speed
                self.dir = 'u'
        if keys[pygame.K_DOWN]:
            if self.rect.y + self.speed < HEIGHT-self.size:
                self.image = link_down
                self.rescale()
                self.rect.y = self.rect.y + self.speed
                self.dir = 'd'
        if keys[pygame.K_SPACE]:            
            Sword(*self.sword_coords()).blit()

    def update(self):
        self.move()
        self.blit()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player,x, y, speed,radius,image,size):
        super().__init__()
        self.player = player 
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.image = image
        self.radius = radius 
        self.rescale()
        self.rect = self.image.get_rect(bottomleft=(self.x,self.y))
        Enemies.add(self)
        self.dir = None
        self.dirs = ["n","s","e","w"] 
    def blit(self):
        screen.blit(self.image,self.rect)
    def rescale(self):
        self.image = pygame.transform.scale(self.image, (self.size,self.size))
    def find_player(self):
        x_dis = self.rect.x - self.player.rect.x 
        y_dis = self.rect.y - self.player.rect.y
        if math.sqrt(x_dis**2 + y_dis**2)<=WIDTH/self.radius:
            if x_dis >0:
                self.rect.x -= self.speed                
            if x_dis<0:
                self.rect.x +=self.speed                  
            if y_dis>0:
                self.rect.y -=self.speed                  
            if y_dis<0:
                self.rect.y +=self.speed
            self.dir = None                     
        else:
            if self.dir == None:
                self.dir = random.choice(self.dirs)            
        return self.dir    

    def update(self):
        self.find_player() 
        if self.dir!=None:
            if self.dir == 'n':
                if self.rect.y - self.speed  >0:
                    self.rect.y -=self.speed
                else:
                    self.dir = 's'    
                
            elif self.dir == 's':
                if self.rect.y + self.speed < HEIGHT-self.size:
                    self.rect.y +=self.speed         
                else:
                    self.dir ='n'
                
            elif self.dir == "e":
                if self.rect.x + self.speed + self.size <WIDTH:
                    self.rect.x +=self.speed
                else:
                    self.dir ='w'
                
            elif self.dir == "w":
                if self.rect.x - self.speed >0:

                    self.rect.x -=self.speed
                else:
                    self.dir = 'e'                
            return                    

class Game:
    def __init__(self):
        self.player_sprite = Player(WIDTH/2, HEIGHT/2)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.enemies = Enemies
        self.build_enemies()

    def build_enemies(self):
        for _ in range(10):
            x = random.randint(100,WIDTH-100)
            y = random.randint(100,HEIGHT-100)
            r = random.randint(2,6)
            s = random.uniform(1.0, 1.9)           
            Enemy(self.player_sprite,x,y,s,r, ghost,75)

    def run(self):
        self.player_sprite.update()
        for enemy in self.enemies:
            enemy.update()
            enemy.blit()
g = Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(BG_Color)
    g.run()
    pygame.display.update()
    clock.tick(60)