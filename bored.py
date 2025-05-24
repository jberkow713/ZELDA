import random 
import pygame
import sys  

WIDTH = 700
HEIGHT = 700
FPS = 60
# Colors
GROUND_COLOR = (255, 222, 179)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (255,0,255)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Drawing Rectangle

class Board:
    def __init__(self, size, loc):
        self.size = size
        self.rect = pygame.Rect(*loc)
        self.speed = 5
    def blit(self):
        pygame.draw.rect(screen,BLUE,self.rect)    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.left= max(0,self.rect.left-self.speed) 
        if keys[pygame.K_RIGHT]:
            self.rect.right = min(WIDTH,self.rect.right +self.speed)
        if keys[pygame.K_UP]:
            self.rect.top = max(0,self.rect.top-self.speed)
        if keys[pygame.K_DOWN]:
            self.rect.bottom = min(HEIGHT, self.rect.bottom+self.speed)

b = Board(100,[50,50,50,50])
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
           
    screen.fill(WHITE)
    b.move()
    b.blit()  
    pygame.display.flip()
