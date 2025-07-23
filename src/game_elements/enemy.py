# src/game_elements/enemy.py
import pygame
import random
from constants import ENEMY1, ENEMY2, AZUL, ANCHO_PANTALLA, ALTO_PANTALLA

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40)) 
       

        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(0,ANCHO_PANTALLA - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad_y = random.randrange(1, 8)
        if self.velocidad_y > 6:
            self.image.fill(ENEMY1)
        elif self.velocidad_y>3:
            self.image.fill(ENEMY2)
        else:
            self.image.fill(AZUL)
    def update(self):
        self.rect.y += self.velocidad_y

        if self.rect.top > ALTO_PANTALLA:
            self.kill()