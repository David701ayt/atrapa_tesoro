import pygame

# 1. Inicializar Pygame
pygame.init()

# 2. Configuración de la Ventana
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("El Cuadrado Mágico")

# 3. Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
NEGRO = (0, 0, 0)

# 4. Propiedades del Jugador (el Cuadrado)
cuadrado_tamano = 50
cuadrado_x = (ANCHO_PANTALLA - cuadrado_tamano) // 2 # Centrado horizontal
cuadrado_y = (ALTO_PANTALLA - cuadrado_tamano) // 2  # Centrado vertical
cuadrado_velocidad = 5

# 5. Bucle Principal del Juego
juego_corriendo = True
reloj = pygame.time.Clock() # Para controlar la velocidad del juego

while juego_corriendo:
    # 6. Manejo de Eventos (entrada del usuario, cerrar ventana)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: # Si el usuario cierra la ventana
            juego_corriendo = False
        
        # Detectar si se presiona una tecla
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                cuadrado_x -= cuadrado_velocidad
            if evento.key == pygame.K_RIGHT:
                cuadrado_x += cuadrado_velocidad
            if evento.key == pygame.K_UP:
                cuadrado_y -= cuadrado_velocidad
            if evento.key == pygame.K_DOWN:
                cuadrado_y += cuadrado_velocidad

    # 7. Actualizar la Lógica del Juego (en este caso, ya lo hicimos con el movimiento)
    # Asegurarse de que el cuadrado no se salga de la pantalla
    if cuadrado_x < 0: cuadrado_x = 0
    if cuadrado_x > ANCHO_PANTALLA - cuadrado_tamano: cuadrado_x = ANCHO_PANTALLA - cuadrado_tamano
    if cuadrado_y < 0: cuadrado_y = 0
    if cuadrado_y > ALTO_PANTALLA - cuadrado_tamano: cuadrado_y = ALTO_PANTALLA - cuadrado_tamano

    # 8. Dibujar / Renderizar
    PANTALLA.fill(NEGRO) # Rellenar el fondo de negro en cada frame
    pygame.draw.rect(PANTALLA, ROJO, (cuadrado_x, cuadrado_y, cuadrado_tamano, cuadrado_tamano))

    # 9. Actualizar la Pantalla
    pygame.display.flip() # O pygame.display.update()

    # 10. Controlar la Velocidad de Fotogramas (FPS)
    reloj.tick(60) # Limitar a 60 fotogramas por segundo

# 11. Salir de Pygame
pygame.quit()