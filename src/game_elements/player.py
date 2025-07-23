# src/game_elements/player.py
import pygame
from constants import ROJO, ANCHO_PANTALLA, ALTO_PANTALLA, AZUL

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Llama al constructor de pygame.sprite.Sprite

        self.image = pygame.Surface((50, 50)) # La imagen del jugador es un cuadrado
        self.image.fill(ROJO) # Color del cuadrado

        self.rect = self.image.get_rect() # Obtiene el rectángulo que representa la posición y tamaño
        self.rect.centerx = ANCHO_PANTALLA // 2
        self.rect.bottom = ALTO_PANTALLA - 10 # Cerca del borde inferior

        self.velocidad = 5
        self.vida = 3 # El jugador tiene 3 vidas
        self.color_original = ROJO # Vamos a guardar el color inicial del jugador

    def update(self):
        # Manejo de la entrada del teclado para el movimiento
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        # Limitar al jugador a la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO_PANTALLA:
            self.rect.right = ANCHO_PANTALLA
    def recibir_danio(self):
        self.vida -= 1
        print(f"Jugador golpeado!! Vida restante: {self.vida}")
        self.image.fill(AZUL) # Cambia temporalmente el color al ser golpeado