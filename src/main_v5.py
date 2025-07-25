# src/main.py
import pygame
import random
from constants import (
    ANCHO_PANTALLA, ALTO_PANTALLA, TITULO_JUEGO, NEGRO, ROJO, AZUL, BLANCO,
    GRIS_OSCURO, STATE_PLAYING, STATE_GAME_OVER, STATE_MENU, GRIS_CLARO
)
from game_elements.player import Player
from game_elements.bullet import Bullet
from game_elements.enemy import Enemy

# 1. Inicializar Pygame
pygame.init()

# 2. Configuración de la Ventana
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption(TITULO_JUEGO)

# --- Configuración de Fuentes ---
fuente_titulo = pygame.font.Font(None, 74) # Para el título del juego / Game Over
fuente_mensaje = pygame.font.Font(None, 48) # Para mensajes como "Presiona R para reiniciar"
fuente_puntuacion = pygame.font.Font(None, 36) # Para la puntuación en juego

# --- Variables del Juego (NUEVAS: Ahora inicializadas en la función reset_game) ---
juego_corriendo = True
current_state = STATE_MENU # ¡El juego empieza en el estado de Menú!

# Grupos de sprites (declarados globalmente para ser accesibles)
todas_las_sprites = pygame.sprite.Group()
balas = pygame.sprite.Group()
enemies = pygame.sprite.Group()
jugador = None # El jugador se creará en reset_game

# Variables para control de tiempo de enemigos (también en reset_game)
ultimo_enemigo_tiempo = 0
tiempo_entre_enemigos = 1000

# Puntuación
puntuacion = 0

# --- Función para Reiniciar/Inicializar el Juego --- (NUEVA)
def reset_game():
    global jugador, todas_las_sprites, balas, enemies, puntuacion, ultimo_enemigo_tiempo, current_state
    
    # Limpiar todos los grupos de sprites
    todas_las_sprites.empty()
    balas.empty()
    enemies.empty()

    # Reinicializar variables del juego
    puntuacion = 0
    jugador = Player()
    todas_las_sprites.add(jugador)

    # Generar enemigos iniciales
    for i in range(5):
        generar_enemigo()
    
    ultimo_enemigo_tiempo = pygame.time.get_ticks() # Resetear el tiempo de generación
    current_state = STATE_PLAYING # Cambiar el estado a "Jugando"

# --- Función para generar un nuevo enemigo (ya existente, pero ahora llamada por reset_game) ---
def generar_enemigo():
    enemigo = Enemy()
    todas_las_sprites.add(enemigo)
    enemies.add(enemigo)

# --- Funciones para dibujar texto en pantalla --- (NUEVAS)
def dibujar_texto(superficie, texto, fuente, color, x, y):
    texto_superficie = fuente.render(texto, True, color)
    texto_rect = texto_superficie.get_rect()
    texto_rect.center = (x, y)
    superficie.blit(texto_superficie, texto_rect)

# --- Configuración de Fondo de Estrellas (igual que antes) ---
estrellas = []
for _ in range(100):
    x = random.randrange(0, ANCHO_PANTALLA)
    y = random.randrange(0, ALTO_PANTALLA)
    velocidad = random.randrange(1, 3)
    estrellas.append([x, y, velocidad])

# --- Bucle Principal del Juego ---
reloj = pygame.time.Clock()

# Inicializar el juego por primera vez al iniciar (entrar al menú)
# No llamamos a reset_game() aquí, porque queremos empezar en el menú.
# El primer reset_game() se llamará cuando el jugador presione una tecla en el menú.

while juego_corriendo:
    # --- Manejo de Eventos Global (para todos los estados) ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            juego_corriendo = False
        
        # --- Lógica de Manejo de Teclas por Estado (NUEVA) ---
        if evento.type == pygame.KEYDOWN:
            if current_state == STATE_MENU:
                reset_game() # Presionar cualquier tecla para iniciar el juego
            elif current_state == STATE_GAME_OVER:
                if evento.key == pygame.K_r: # Presionar 'R' para reiniciar
                    reset_game()
            elif current_state == STATE_PLAYING:
                if evento.key == pygame.K_SPACE:
                    if jugador.vida > 0:
                        bala = Bullet(jugador.rect.centerx, jugador.rect.top)
                        todas_las_sprites.add(bala)
                        balas.add(bala)

    # --- Lógica de Actualización y Dibujo Basada en el Estado del Juego (NUEVA) ---
    if current_state == STATE_PLAYING:
        # Actualizar la Lógica del Juego (solo si estamos jugando)
        todas_las_sprites.update()

        # Generar enemigos periódicamente
        ahora = pygame.time.get_ticks()
        if ahora - ultimo_enemigo_tiempo > tiempo_entre_enemigos:
            ultimo_enemigo_tiempo = ahora
            generar_enemigo()

        # Colisiones entre balas y enemigos
        colisiones_balas_enemigos = pygame.sprite.groupcollide(balas, enemies, True, True)
        for bala_colisionada, enemigos_golpeados in colisiones_balas_enemigos.items():
            for enemigo_golpeado in enemigos_golpeados:
                puntuacion += enemigo_golpeado.puntos
            if not enemies:
                for _ in range(5):
                    generar_enemigo()

        # Colisiones entre jugador y enemigos
        colisiones_jugador_enemigos = pygame.sprite.spritecollide(jugador, enemies, True)
        for enemigo_colisionado in colisiones_jugador_enemigos:
            jugador.recibir_danio()
            if jugador.vida <= 0:
                print("¡Juego Terminado! El jugador se quedó sin vida.")
                current_state = STATE_GAME_OVER # Cambiar al estado de Game Over
            generar_enemigo()

        # Actualizar Fondo de Estrellas (solo si estamos jugando)
        for estrella in estrellas:
            estrella[1] += estrella[2]
            if estrella[1] > ALTO_PANTALLA:
                estrella[1] = 0
                estrella[0] = random.randrange(0, ANCHO_PANTALLA)

        # Dibujar / Renderizar (solo si estamos jugando)
        PANTALLA.fill(NEGRO) # Rellenar el fondo de negro

        # Dibujar las estrellas
        for estrella in estrellas:
            pygame.draw.circle(PANTALLA, BLANCO, (estrella[0], estrella[1]), 1)

        todas_las_sprites.draw(PANTALLA)

        # Dibujar la Puntuación y Vida
        texto_puntuacion_surface = fuente_puntuacion.render(f"Puntos: {puntuacion}", True, BLANCO)
        PANTALLA.blit(texto_puntuacion_surface, (10, 10))
        
        texto_vida_surface = fuente_puntuacion.render(f"Vida: {jugador.vida}", True, BLANCO)
        PANTALLA.blit(texto_vida_surface, (ANCHO_PANTALLA - texto_vida_surface.get_width() - 10, 10))

    elif current_state == STATE_MENU:
        PANTALLA.fill(NEGRO)
        dibujar_texto(PANTALLA, TITULO_JUEGO, fuente_titulo, BLANCO, ANCHO_PANTALLA // 2, ALTO_PANTALLA // 3)
        dibujar_texto(PANTALLA, "Presiona cualquier tecla para empezar", fuente_mensaje, GRIS_CLARO, ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2)

    elif current_state == STATE_GAME_OVER:
        PANTALLA.fill(NEGRO)
        dibujar_texto(PANTALLA, "¡JUEGO TERMINADO!", fuente_titulo, ROJO, ANCHO_PANTALLA // 2, ALTO_PANTALLA // 3)
        dibujar_texto(PANTALLA, f"Puntuación Final: {puntuacion}", fuente_mensaje, BLANCO, ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2)
        dibujar_texto(PANTALLA, "Presiona 'R' para reiniciar", fuente_mensaje, GRIS_CLARO, ANCHO_PANTALLA // 2, ALTO_PANTALLA * 2 // 3)

    # 8. Actualizar la Pantalla (siempre se actualiza)
    pygame.display.flip()

    # 9. Controlar la Velocidad de Fotogramas (FPS)
    reloj.tick(60)

# 10. Salir de Pygame
pygame.quit()