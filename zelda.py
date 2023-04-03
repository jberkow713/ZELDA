import pygame
import random
from sys import exit
from pygame.locals import  *
import copy
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

class Player:
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.size = 75 
        self.image = link_down
        self.rescale()
        self.rect = self.image.get_rect(bottomleft=(self.x,self.y))
        self.speed = 5   
    
    def rescale(self):
        self.image = pygame.transform.scale(self.image, (self.size,self.size))

    def blit(self):
        screen.blit(self.image,self.rect)
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.rect.x + self.speed <= WIDTH - self.size:
                self.image = link_right
                self.rescale()
                self.rect.x +=self.speed 
        if keys[pygame.K_LEFT]:
            if self.rect.x - self.speed >0:
                self.image = link_left
                self.rescale()
                self.rect.x -=self.speed
        if keys[pygame.K_UP]:
            if self.rect.y - self.speed > 0:
                self.image = link_up
                self.rescale()
                self.rect.y =self.rect.y - self.speed
        if keys[pygame.K_DOWN]:
            if self.rect.y + self.speed < HEIGHT-self.size:
                self.image = link_down
                self.rescale()
                self.rect.y = self.rect.y + self.speed
                
p = Player(WIDTH/2, HEIGHT/2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(BG_Color)
    p.blit()
    p.move()
    pygame.display.update()
    clock.tick(60)