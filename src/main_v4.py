# src/main.py
import pygame
import random
from constants import ANCHO_PANTALLA, ALTO_PANTALLA, TITULO_JUEGO, NEGRO, ROJO, AZUL, BLANCO, GRIS_OSCURO # Importa los nuevos colores
from game_elements.player import Player
from game_elements.bullet import Bullet
from game_elements.enemy import Enemy

# 1. Inicializar Pygame
pygame.init()

# 2. Configuración de la Ventana
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption(TITULO_JUEGO)

# --- Configuración de Puntuación y Fuentes ---
puntuacion = 0
fuente_puntuacion = pygame.font.Font(None, 36) # Fuente por defecto de Pygame, tamaño 36

# --- Configuración de Fondo de Estrellas ---
# Creamos una lista de estrellas (posición x, posición y, velocidad)
estrellas = []
for _ in range(100): # 100 estrellas
    x = random.randrange(0, ANCHO_PANTALLA)
    y = random.randrange(0, ALTO_PANTALLA)
    velocidad = random.randrange(1, 3) # Algunas se mueven más rápido
    estrellas.append([x, y, velocidad])


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
                # Asegurarse de que el jugador aún esté vivo para disparar
                if jugador.vida > 0:
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
    colisiones_balas_enemigos = pygame.sprite.groupcollide(balas, enemies, True, True)
    for bala_colisionada, enemigos_golpeados in colisiones_balas_enemigos.items():
        for enemigo_golpeado in enemigos_golpeados:
            puntuacion += enemigo_golpeado.puntos # Sumar puntos por cada enemigo destruido
            print(f"¡Enemigo destruido! Puntuación: {puntuacion}")
        
        if not enemies:
            for _ in range(5):
                generar_enemigo()

    # Colisiones entre jugador y enemigos
    colisiones_jugador_enemigos = pygame.sprite.spritecollide(jugador, enemies, True)
    for enemigo_colisionado in colisiones_jugador_enemigos:
        jugador.recibir_danio()
        if jugador.vida <= 0:
            print("¡Juego Terminado! El jugador se quedó sin vida.")
            juego_corriendo = False
        generar_enemigo()
    
    # --- Actualizar Fondo de Estrellas ---
    for estrella in estrellas:
        estrella[1] += estrella[2] # Mover estrella hacia abajo
        if estrella[1] > ALTO_PANTALLA: # Si sale de la pantalla, moverla arriba
            estrella[1] = 0
            estrella[0] = random.randrange(0, ANCHO_PANTALLA) # Nueva posición X aleatoria

    # 7. Dibujar / Renderizar
    PANTALLA.fill(NEGRO) # Rellenar el fondo de negro

    # Dibujar las estrellas
    for estrella in estrellas:
        pygame.draw.circle(PANTALLA, BLANCO, (estrella[0], estrella[1]), 1) # Dibujar un pequeño círculo blanco

    todas_las_sprites.draw(PANTALLA)

    # Dibujar la Puntuación
    texto_puntuacion = fuente_puntuacion.render(f"Puntos: {puntuacion}", True, BLANCO) # Renderizar el texto
    PANTALLA.blit(texto_puntuacion, (10, 10)) # Dibujar el texto en la esquina superior izquierda

    # Dibujar la Vida del Jugador (opcional)
    texto_vida = fuente_puntuacion.render(f"Vida: {jugador.vida}", True, BLANCO)
    PANTALLA.blit(texto_vida, (ANCHO_PANTALLA - texto_vida.get_width() - 10, 10))


    # 8. Actualizar la Pantalla
    pygame.display.flip()

    # 9. Controlar la Velocidad de Fotogramas (FPS)
    reloj.tick(60)

# 10. Salir de Pygame
pygame.quit()