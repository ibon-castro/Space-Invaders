import pygame
from pygame import mixer
import random
import math
import operator


pygame.init()

screen = pygame.display.set_mode((800,600))

fondo = pygame.image.load('background.jpg')
fondo = pygame.transform.scale(fondo, (800,600))

mixer.music.load('sonidofondo.wav')
mixer.music.play(-1)

pygame.display.set_caption('Deusto Invaders')
logo = pygame.image.load('logo.png')
pygame.display.set_icon(logo)
trofeo = pygame.image.load('copa.png')
trofeo = pygame.transform.scale(trofeo,(100,100))

deusto_imagen = pygame.image.load('deusto.png')
fuente = pygame.font.Font('freesansbold.ttf',30)


fichero = open('ranking.csv','a+')


def ranking():
    rank = True
    while rank:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        letra = pygame.font.Font ('freesansbold.ttf',54)        
        texto_ranking = letra.render('RANKING', True, (0,255,255))
        screen.blit(trofeo,(25,25))
        screen.blit(trofeo,(675,25))
        screen.blit(texto_ranking,(250,50))
        diccionario = {}
        fichero = open('ranking.csv')
        for linea in fichero:
            linea = linea.strip('\n')
            (key,val) = linea.split(';')
            diccionario[key] = val

        diccionario_ordenar = dict(sorted(diccionario.items(), key=operator.itemgetter(1), reverse=True))

        nombres = list(diccionario_ordenar.keys())
        resultados = list(diccionario_ordenar.values())


        primero = f'1º {nombres[0].upper()} {resultados[0]}'
        segundo = f'2º {nombres[1].upper()} {resultados[1]}'
        tercero = f'3º {nombres[2].upper()} {resultados[2]}'
        cuarto = f'4º {nombres[3].upper()} {resultados[3]}'
        quinto = f'5º {nombres[4].upper()} {resultados[4]}'

        primero_texto = letra.render(primero, True, (255,255,255))
        segundo_texto = letra.render(segundo, True, (255,255,255))
        tercero_texto = letra.render(tercero, True, (255,255,255))
        cuarto_texto = letra.render(cuarto, True, (255,255,255))
        quinto_texto = letra.render(quinto, True, (255,255,255))

        screen.blit(primero_texto,(150,100))
        screen.blit(segundo_texto,(150,200))
        screen.blit(tercero_texto,(150,300))
        screen.blit(cuarto_texto,(150,400))
        screen.blit(quinto_texto,(150,500))

        boton(650, 525, 120, 60, (0,0,255),(0,0,200),menu_inicial)

        volver_menu = fuente.render('Menu', True, (255,255,255))
        screen.blit(volver_menu, (670,540))

        
        

        

        pygame.display.update()

def menu_inicial():
    menu = True
    while menu:
        screen.fill((4,60,164))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        letra = pygame.font.Font ('freesansbold.ttf',60)
        texto_menu = letra.render('DEUSTO INVADERS', True, (63,231,103))
        texto_autor = fuente.render('By: Ibon Castro', True, (255,255,255))
        controles = fuente.render('Muevete con las flechas y dispara con CTRL', True, (221,70,127))
        screen.blit(texto_menu,(110,50))
        screen.blit(texto_autor,(275,550))
        screen.blit(deusto_imagen,(250,200))
        screen.blit(controles,(80,175))
        boton(50,425,200,75,(255,0,0),(200,0,0),juego)
        boton(525,425,200,75,(0,255,0),(0,200,0),ranking)
        letra_botones = pygame.font.Font('freesansbold.ttf',30)
        boton1 = letra_botones.render('JUGAR', True, (255,255,255))
        boton2 = letra_botones.render('RANKING', True, (255,255,255))
        screen.blit(boton1,(95,450))
        screen.blit(boton2,(550,450))
        pygame.display.update()



def boton(x,y,w,h,c1,c2,accion=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, c1, (x,y,w,h))
        if click[0] == 1 and accion != None:
            if accion() == 'jugar':
                juego()
            elif accion() == 'menu_inicial':
                menu_inicial()
            elif accion() == 'rank':
                ranking()
    else:
        pygame.draw.rect(screen, c2, (x,y,w,h))

        


def juego():
    aliado_imagen = pygame.image.load('ufo.png')
    aliado_imagen = pygame.transform.scale(aliado_imagen, (100,100))
    aliadoX = 650
    aliadoY = 250
    aliadoX_cambio = 0
    aliadoY_cambio = 0

    enemigo_imagen = []
    enemigoX = []
    enemigoY = []
    enemigoX_cambio = []
    enemigoY_cambio = []
    numero_de_enemigos = 5
    
    for i in range(numero_de_enemigos):
        enemigo_imagen.append(pygame.image.load('spaceship.png'))
        enemigoX.append(random.randint(100,150))
        enemigoY.append(random.randint(150,525))
        enemigoX_cambio.append(35)
        enemigoY_cambio.append(0.4)
        enemigo_imagen[i]= pygame.transform.scale(enemigo_imagen[i], (75,75))


    bala_imagen = pygame.image.load('bullet.png')
    bala_imagen = pygame.transform.scale(bala_imagen, (25,25))
    balaX = aliadoX
    balaY = aliadoY
    balaX_cambio = 1
    bala_estado = 'preparado'

    result = 0


    fuente = pygame.font.Font('freesansbold.ttf',40)
    textoX = 10
    textoY = 10

    final = pygame.font.Font('freesansbold.ttf', 88)

    texto = ''
    rectangulo_usuario = pygame.Rect(250, 300, 140, 64)
    color = (255,255,255)


    def final_partida(x,y):
        screen.fill((0,0,0))
        gameover = final.render('GAME OVER', True, (255, 0, 0))
        datos = fuente.render('Pon tu nombre aqui', True, (160,160,160))
        guardar_datos = fuente.render('Presiona INTRO para guardar tus datos', True, (160,160,160))
        restart = fuente.render('Presiona TAB para comenzar de nuevo', True, (0,255,0))
        menu = fuente.render('Menu', True, (255,255,255))
        screen.blit(gameover, (x, y))
        screen.blit(restart,(25,525))
        screen.blit(datos, (225, 225))
        screen.blit(guardar_datos, (15,175))
        boton(300,450,200,50,(0,0,255),(0,0,200),menu_inicial)
        screen.blit(menu, (345,457))



    def enseñar_resultado(x,y):
        resultado = fuente.render('Resultado: ' + str(result), True, (255,255,255))
        screen.blit(resultado,(x,y))
        
    def aliado(x,y):
        screen.blit(aliado_imagen,(x, y))

    def enemigo(x,y,i):
        screen.blit(enemigo_imagen[i],(x,y))
    
    def bala(x,y):
        screen.blit (bala_imagen,(x,y + 32))

    def colision(enemigoX,enemigoY,balaX,balaY):
        distancia = math.sqrt((math.pow(enemigoX - balaX, 2)) + (math.pow(enemigoY - balaY, 2)))
        if distancia < 50:
            return True
        else: 
            return False


    funciona = True
    while funciona:
        screen.fill((0,0,0))
        screen.blit(fondo,(0,0))
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    aliadoX_cambio = -0.4
                elif event.key == pygame.K_RIGHT:
                    aliadoX_cambio = 0.4
                elif event.key == pygame.K_UP:
                    aliadoY_cambio = -0.4
                elif event.key == pygame.K_DOWN:
                    aliadoY_cambio = 0.4
                elif event.key == pygame.K_LCTRL:
                    bala_estado = 'disparar'
                    balaY = aliadoY
                    bala(balaX,balaY)
                    sonido_bala = mixer.Sound('sonidodisparo.wav')
                    sonido_bala.play()
                elif event.key == pygame.K_TAB and aliadoX > 900:
                    juego()
                elif event.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                elif event.key == pygame.K_RETURN:
                    texto = texto.strip()
                    resultado = str(result).zfill(3)
                    fichero.write(f'''{texto};{resultado}\n''')
                    texto = ''
                else:
                    texto += event.unicode
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    aliadoX_cambio = 0
                    aliadoY_cambio = 0
                

        aliadoX += aliadoX_cambio
        aliadoY += aliadoY_cambio

        if aliadoY <= 0:
            aliadoY = 0
        elif aliadoY >= 500:
            aliadoY = 500
        elif aliadoX >= 720:
            aliadoX = 720
        elif aliadoX <= 100:
            aliadoX = 100

        
        enemigoY += enemigoY_cambio
        for i in range(numero_de_enemigos):
            enemigoY[i] += enemigoY_cambio[i]
            if enemigoY[i] <= 10:
                enemigoY_cambio[i] = 0.4
                if 10 > result >= 5:
                    enemigoY_cambio[i] = 0.6
                elif 15 > result >= 10:
                    enemigoY_cambio[i] = 0.8
                elif 20 > result >= 15:
                    enemigoY_cambio[i] = 1
                elif 25 > result >= 20:
                    enemigoY_cambio[i] = 1.25
                elif result >= 25:
                    enemigoY_cambio[i] = 1.5
                enemigoX[i] += enemigoX_cambio[i]
            elif enemigoY[i] >= 525:
                enemigoY_cambio[i] = -0.4
                if 10 > result >= 5:
                    enemigoY_cambio[i] = -0.6
                elif 15 > result >= 10:
                    enemigoY_cambio[i] = -0.8
                elif 20 > result >= 15:
                    enemigoY_cambio[i] = -1
                elif 25> result >= 20:
                    enemigoY_cambio[i] = -1.25
                elif result >= 25:
                    enemigoY_cambio[i] = -1.5
                enemigoX[i] += enemigoX_cambio[i]
            
            
            
            colision_final = colision(enemigoX[i], enemigoY[i], balaX, balaY)
            if colision_final:
                balaX = aliadoX
                bala_estado = 'preparado'
                result += 1
                enemigoX[i] = random.randint(50,100)
                enemigoY[i] = random.randint(100,300)
                sonido_explosion = mixer.Sound('sonidoexplosion.wav')
                sonido_explosion.play()

            
            enemigo(enemigoX[i], enemigoY[i], i)
            if enemigoX[i]>aliadoX:
                for j in range (numero_de_enemigos):
                    enemigoX[j] = 1000
                aliadoX = 950
                bala_estado = 'preparado'
                final_partida(125,50)
                pygame.draw.rect(screen,color,rectangulo_usuario)
                texto_usuario = fuente.render(texto, True, (0,0,0))
                rectangulo_usuario.w = max(100,texto_usuario.get_width()+10)
                screen.blit(texto_usuario, (rectangulo_usuario.x, rectangulo_usuario.y))
                

                


        if balaX <= 0:
            balaX = aliadoX
            bala_estado = 'preparado'


        if bala_estado == 'disparar':
            bala(balaX, balaY)
            balaX -= balaX_cambio



        
        aliado(aliadoX, aliadoY)
        enseñar_resultado(textoX,textoY)
        
        pygame.display.update()

menu_inicial()

