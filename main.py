import pygame, sys
from pygame.locals import *
import random, time

from enemy import Enemy
from hero import Hero
from config import *



pygame.init()

FramePerSec = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((600,400))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


user = Hero("Absolute")
firstEnemy = Enemy(100, 20, "Sludge Guy")

enemies = pygame.sprite.Group()
enemies.add(firstEnemy)
all_sprites = pygame.sprite.Group()
all_sprites.add(user)
all_sprites.add(firstEnemy)

while True:
       
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
 
    DISPLAYSURF.fill(WHITE)
 
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        if isinstance(entity, Hero):
            entity.update()
        # elif isinstance(entity, Enemy):
        #     entity.move()
 
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(user, enemies):
          DISPLAYSURF.fill(RED)
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()        
         
    pygame.display.update()
    FramePerSec.tick(FPS)
    

