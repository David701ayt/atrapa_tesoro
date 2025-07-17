# src/main.py
import pygame
from constants import ANCHO_PANTALLA, ALTO_PANTALLA, TITULO_JUEGO, NEGRO, ROJO # Importa solo lo necesario
from game_elements.player import Player
from game_elements.bullet import Bullet
from game_elements.enemy import Enemy
import random
# 1. Inicializar Pygame
pygame.init()

# 2. Configuración de la Ventana
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption(TITULO_JUEGO)

# 3. Inicializar objetos del juego
jugador = Player() # Creamos una instancia de nuestra clase Player

# Grupos de sprites
# Un 'Group' en Pygame es una forma eficiente de manejar un conjunto de sprites
todas_las_sprites = pygame.sprite.Group()
balas = pygame.sprite.Group()
enemies = pygame.sprite.Group()

todas_las_sprites.add(jugador) # Añadimos el jugador al grupo de todas las sprites

def generar_enemigo():
    enemigo = Enemy()
    todas_las_sprites.add(enemigo)
    enemies.add(enemigo)
cantidad_enemigos = random.randrange(2,10)
for i in range(cantidad_enemigos):
    generar_enemigo()
ultimo_enemigo_tiempo = pygame.time.get_ticks()
tiempo_entre_enemigos = 1000 

# 4. Bucle Principal del Juego
juego_corriendo = True
reloj = pygame.time.Clock()

while juego_corriendo:
    # 5. Manejo de Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            juego_corriendo = False
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                # Crear una nueva bala desde la posición del jugador
                # Usamos jugador.rect.centerx y jugador.rect.top para posicionar la bala
                bala = Bullet(jugador.rect.centerx, jugador.rect.top)
                todas_las_sprites.add(bala)
                balas.add(bala)

    # 6. Actualizar la Lógica del Juego
    todas_las_sprites.update() # Llama al método .update() de todas las sprites en el grupo

    ahora = pygame.time.get_ticks()
    if ahora - ultimo_enemigo_tiempo > tiempo_entre_enemigos:
        ultimo_enemigo_tiempo = ahora
        generar_enemigo()

    # 7. Dibujar / Renderizar
    PANTALLA.fill(NEGRO) # Rellenar el fondo de negro en cada frame

    todas_las_sprites.draw(PANTALLA) # Dibujar todas las sprites en la pantalla

    # 8. Actualizar la Pantalla
    pygame.display.flip()

    # 9. Controlar la Velocidad de Fotogramas (FPS)
    reloj.tick(60)

# 10. Salir de Pygame
pygame.quit()