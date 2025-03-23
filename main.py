import pygame
import math
import time
from Utils import escalar_imagen, blit_rotar_centro, blit_text_center
pygame.font.init()
GRASS = escalar_imagen(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = escalar_imagen(pygame.image.load("imgs/track.png"), 0.9)
TRACK_BORDER = escalar_imagen(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = pygame.image.load("imgs/finish.png")
FINISH_POSITION = (130, 250)
FINISH_MASK = pygame.mask.from_surface(FINISH)
GREEN_CAR = escalar_imagen(pygame.image.load("imgs/green-car.png"), 0.55)
RED_CAR =  escalar_imagen(pygame.image.load("imgs/red-car.png"), 0.55)
GREY_CAR = escalar_imagen(pygame.image.load("imgs/grey-car.png"), 0.55)
PURPLE_CAR = escalar_imagen(pygame.image.load("imgs/purple-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing game!")
MAIN_FONT = pygame.font.SysFont("comicsans", 44)

fps = 60
PATH = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551), (613, 715), (736, 713),
        (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]

class informacionJuego:
    NIVELES = 10

    def __init__(self, level = 1):
        self.level = level
        self.iniciado = False
        self.nivel_tiempo_inicio = 0

    def siguiente_nivel(self):
        self.level += 1
        self.iniciado = False

    def reinicio(self):
        self.level = 1
        self.iniciado = False
        self.nivel_tiempo_inicio = 0

    def juego_terminado(self):
        return self.level > self.NIVELES

    def iniciarNivel(self):
        self.iniciado = True
        self.nivel_tiempo_inicio = time.time()

    def getLevelTime(self):
        if not self.iniciado:
            return 0
        return round(time.time() - self.nivel_tiempo_inicio)







def dibujar(win, images, JugadorCarro, ComputadoraCarro):
    for img, pos in images:
        win.blit(img, pos)
    level_text =  MAIN_FONT.render(f"Nivel: {game_info.level}",1,(255,255,255))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))
    time_text = MAIN_FONT.render(f"Tiempo: {round(game_info.getLevelTime(),1)} s", 1, (255, 255, 255))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))
    vel_text = MAIN_FONT.render(f"Velocidad: {round(JugadorCarro.vel,1)} px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))
    JugadorCarro.dibujar(win)
    ComputadoraCarro.dibujar(win)
    pygame.display.update()






class AbstractCar:
    def __init__(self, max_vel, rotacion_vel):
        self.img = self.IMG
        self.max_vel = max_vel

        self.rotacion_vel = rotacion_vel
        self.vel = 0
        self.angulo = 0
        self.x, self.y = self.POSICION_INICIAL
        self.aceleracion = 0.1

    def rotacion (self, left = False, right = False):
        if left:
            self.angulo += self.rotacion_vel
        elif right:
            self.angulo -= self.rotacion_vel

    def dibujar(self, win):
        blit_rotar_centro(win, self.img,(self.x, self.y), self.angulo)

    def moverAdelante(self):
        self.vel = min(self.vel  + self.aceleracion, self.max_vel)
        self.move()

    def move(self):
        radianes = math.radians(self.angulo)
        vertical = math.cos(radianes) * self.vel
        horizontal = math.sin(radianes) * self.vel
        self.y -= vertical
        self.x -= horizontal



    def moverAtras(self):
        self.vel = max(self.vel - self.aceleracion, -self.max_vel/2)
        self.move()

    def colision(self, mask, x=0, y=0):
        carro_mascara = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(carro_mascara, offset)
        return poi

    def reseteo(self):
        self.x, self.y = self.POSICION_INICIAL
        self.angulo = 0
        self.vel = 0

def movimiento_jugador(self, JugadorCarro):
        teclas = pygame.key.get_pressed()
        moviendo = False

        if teclas[pygame.K_a]:
            JugadorCarro.rotacion(left=True)
        if teclas[pygame.K_d]:
            JugadorCarro.rotacion(right=True)
        if teclas[pygame.K_w]:
            moviendo = True
            JugadorCarro.moverAdelante()
        if teclas[pygame.K_s]:
            moviendo = True
            JugadorCarro.moverAtras()
        if not moviendo:
            JugadorCarro.reducir_velocidad()


class Jugador_Carro(AbstractCar):
    IMG = RED_CAR
    POSICION_INICIAL = (180, 200)

    def reducir_velocidad(self):
        self.vel = max(self.vel - self.aceleracion/2, 0)
        self.move()

    def rebotar(self):
        self.vel = -self.vel
        self.move()

class Computadora_Caroo(AbstractCar):
    IMG = GREEN_CAR
    POSICION_INICIAL = (150, 200)
    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.currentPoint = 0
        self.vel = max_vel

    #def dibujarPuntos(self,win):
     #   for point in self.path:
      #      pygame.draw.circle(win, (250, 0 , 0 ), point, 5 )

    def dibujar(self,win):
        super().dibujar(win)
        #self.dibujarPuntos(win)

    def calcularAngulo(self):
        target_x, target_y = self.path[self.currentPoint]
        x_diff = target_x - self.x
        y_diff = target_y - self.y
        if y_diff == 0:
            desired_radian_angle = math.pi/2
        else: desired_radian_angle = math.atan(x_diff/y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angulo - math.degrees(desired_radian_angle)

        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angulo -= min(self.rotacion_vel, abs(difference_in_angle))
        else:
            self.angulo += min(self.rotacion_vel, abs(difference_in_angle))
    def update_path_point(self):
        target = self.path[self.currentPoint]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.currentPoint += 1

    def move(self):
        if self.currentPoint >= len(self.path):
            return
        self.calcularAngulo()
        self.update_path_point()
        super().move()


    def next_level(self, level):
        self.reseteo()
        self.vel = self.max_vel + (level-1) * 0.2
        self.currentPoint = 0




def movimiento_jugador(JugadorCarro):
    teclas = pygame.key.get_pressed()
    moviendo = False

    if teclas[pygame.K_a]:
        JugadorCarro.rotacion(left=True)
    if teclas[pygame.K_d]:
        JugadorCarro.rotacion(right=True)
    if teclas[pygame.K_w]:
        moviendo = True
        JugadorCarro.moverAdelante()
    if teclas[pygame.K_s]:
        moviendo = True
        JugadorCarro.moverAtras()
    if not moviendo:
        JugadorCarro.reducir_velocidad()

def lineaDeMeta(JugadorCarro, ComputadoraCarro, game_info):
    if JugadorCarro.colision(TRACK_BORDER_MASK) != None:
        JugadorCarro.rebotar()
    ColisionComputadora = ComputadoraCarro.colision(FINISH_MASK, *FINISH_POSITION)
    if  ColisionComputadora != None:
        print("Computadora gana")

        blit_text_center(WIN , MAIN_FONT, "Perdiste! ")
        pygame.display.update()
        pygame.time.wait(5000)
        JugadorCarro.reseteo()
        ComputadoraCarro.reseteo()
        game_info.reinicio()


    ColisionJugador = JugadorCarro.colision(FINISH_MASK, *FINISH_POSITION)
    if  ColisionJugador != None:
        if ColisionJugador[1] == 0:
            JugadorCarro.rebotar()
        else:
            game_info.siguiente_nivel()
            JugadorCarro.reseteo()
            ComputadoraCarro.next_level(game_info.level)
            print("Ganaste")



run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]
JugadorCarro = Jugador_Carro(4,4)
ComputadoraCarro= Computadora_Caroo(2,4, PATH)
game_info = informacionJuego()
while run:
    clock.tick(fps)
    dibujar(WIN, images, JugadorCarro, ComputadoraCarro)
    while not game_info.iniciado:
        blit_text_center(WIN, MAIN_FONT, f"Presiona cualquier tecla para iniciar el nivel {game_info.level}")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                game_info.iniciarNivel()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        #if event.type == pygame.MOUSEBUTTONDOWN:
         #   pos = pygame.mouse.get_pos()
          #  ComputadoraCarro.path.append(pos)


    movimiento_jugador(JugadorCarro)
    ComputadoraCarro.move()



    lineaDeMeta(JugadorCarro, ComputadoraCarro, game_info)

    if game_info.juego_terminado():
        blit_text_center(WIN, MAIN_FONT, "Ganaste! ")
        pygame.time.wait(5000)
        JugadorCarro.reseteo()
        ComputadoraCarro.reseteo()
        game_info.reinicio()


#print(ComputadoraCarro.path)
pygame.quit()