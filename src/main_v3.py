# src/main.py
import pygame
import random
from constants import ANCHO_PANTALLA, ALTO_PANTALLA, TITULO_JUEGO, NEGRO, ROJO, AZUL # Importa AZUL también
from game_elements.player import Player
from game_elements.bullet import Bullet
from game_elements.enemy import Enemy

# 1. Inicializar Pygame
pygame.init()

# 2. Configuración de la Ventana
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption(TITULO_JUEGO)

# 3. Inicializar objetos del juego
jugador = Player()

# Grupos de sprites
todas_las_sprites = pygame.sprite.Group()
balas = pygame.sprite.Group()
enemies = pygame.sprite.Group()

todas_las_sprites.add(jugador)

def generar_enemigo():
    enemigo = Enemy()
    todas_las_sprites.add(enemigo)
    enemies.add(enemigo)

for i in range(5):
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
                bala = Bullet(jugador.rect.centerx, jugador.rect.top)
                todas_las_sprites.add(bala)
                balas.add(bala)

    # 6. Actualizar la Lógica del Juego
    todas_las_sprites.update()

    # Generar enemigos periódicamente
    ahora = pygame.time.get_ticks()
    if ahora - ultimo_enemigo_tiempo > tiempo_entre_enemigos:
        ultimo_enemigo_tiempo = ahora
        generar_enemigo()

    # --- Lógica de Detección de Colisiones ---

    # Colisiones entre balas y enemigos
    # groupcollide(grupo1, grupo2, dokill1, dokill2)
    # dokill1=True: Elimina la bala. dokill2=True: Elimina el enemigo.
    colisiones_balas_enemigos = pygame.sprite.groupcollide(balas, enemies, True, True)
    for bala_colisionada, enemigos_golpeados in colisiones_balas_enemigos.items():
        # Cuando una bala golpea uno o más enemigos:
        # En una empresa, aquí aumentarías la puntuación, reproducirías un sonido,
        # mostrarías una explosión, etc.
        print(f"¡Bala eliminó {len(enemigos_golpeados)} enemigo(s)!")
        # Podrías añadir lógica para generar un nuevo enemigo si se elimininan muchos
        # o para que el juego continúe siempre generando.
        # Por simplicidad, volvemos a generar enemigos si no quedan
        if not enemies: # Si no quedan enemigos en pantalla
            for _ in range(5): # Generar un nuevo lote
                generar_enemigo()


    # Colisiones entre jugador y enemigos
    # spritecollide(sprite, group, dokill)
    # dokill=True: Elimina el enemigo que colisiona con el jugador
    colisiones_jugador_enemigos = pygame.sprite.spritecollide(jugador, enemies, True)
    for enemigo_colisionado in colisiones_jugador_enemigos:
        jugador.recibir_danio() # Llama al método de daño del jugador
        if jugador.vida <= 0:
            print("¡Juego Terminado! El jugador se quedó sin vida.")
            juego_corriendo = False # Termina el juego si la vida llega a 0
        # Después de una colisión, también podrías generar un nuevo enemigo
        generar_enemigo()


    # 7. Dibujar / Renderizar
    PANTALLA.fill(NEGRO)

    todas_las_sprites.draw(PANTALLA)

    # 8. Actualizar la Pantalla
    pygame.display.flip()

    # 9. Controlar la Velocidad de Fotogramas (FPS)
    reloj.tick(60)

# 10. Salir de Pygame
pygame.quit()