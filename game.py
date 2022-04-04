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

class Level:
    def __init__(self):
        self.Screen = screen

        self.enemies = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()

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
        
    def rescale(self):
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def move(self, speed):
        
        if self.direction == None:
            self.direction = self.choices[random.randint(0,len(self.choices)-1)]
        
        if self.direction=='R':
            
            if self.x + speed <=WIDTH - .5*self.size: 
                self.x +=speed            
                self.rect.center = (self.x, self.y)
            else:                
                self.direction = 'L'

        elif self.direction == 'L':
            
            if self.x - speed >0+.5*self.size:
                self.x -=speed
                self.rect.center = (self.x, self.y)
            else:
                self.direction = 'R'               
                
        elif self.direction == 'U':
            
            if self.y - speed >0 + .5*self.size:           
            
                self.y -=speed
                self.rect.center = (self.x, self.y)
            else:
                self.direction = 'D'

        elif self.direction == 'D':
            
            if self.y + speed < HEIGHT- .5*self.size:

                self.y +=speed
                self.rect.center = (self.x, self.y)
            else:
                self.direction = 'U'

G = Object(ghost, 700,700,100)
Level1 = Level()

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit() 

    Level1.Screen.fill(GROUND_COLOR)
        
    G.move(4)
    Level1.Screen.blit(G.image, G.rect)  

    pygame.display.flip()



      