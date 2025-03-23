import pygame

def escalar_imagen(img, factor):
    NuevoTamaño = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, NuevoTamaño)

def blit_rotar_centro(win, imagen, top_left, angulo):
    imagen_rotada = pygame.transform.rotate(imagen, angulo)
    nuevo_rect = imagen_rotada.get_rect(center = imagen.get_rect(topleft = top_left).center)
    win.blit(imagen_rotada, nuevo_rect.topleft)

def blit_text_center(win, font, text):
    render = font.render(text, 1 , (200,200,200))
    win.blit(render,(win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2 ))