'Librerias'
import tkinter as tk
from tkinter import *
from tkinter import Tk
import tkinter.font
import random
import pygame
import threading
import os
import os.path
import time




'Cargar Imágenes'
def cargarimg(archivo):
    ruta = os.path.join('Archivos', archivo) #pone la ruta para cargar los archivos
    imagen = PhotoImage(file=ruta)  #hace que se sepa que la imagen está en la ruta
    return imagen

#-------------------Menú Principal------------------------------------------------#
'Ventana Menú'
ven = Tk() #crea la ventana
ven.wm_title("Space Impact") #título
ven.geometry('823x823') #dimensiones
ven.maxsize(width=823, height=823)#para que no se mueva la ventana
ven.minsize(width=823, height=823)

'canva Menú'
menu = Canvas(ven, width=0, height=0, bg='black')#canva para la ventana, alto, anchura y color
menu.pack()
'imagen para menú'
imagenfondo = cargarimg('fondo.png') #imagen para poner de fondo
men_fondo = Label(menu, image=imagenfondo) #pone la imagen en el menú
men_fondo.pack()

'Texto de Menú'
FuenteMenu = tkinter.font.Font(family="Fixedsys", size=30) #fuente para el texto
titulo=tkinter.Label(ven, text='Space Impact', font=FuenteMenu, bg='black', fg='white')#Texto y fuente insertada
titulo.place(relx=0.5, rely=0.25, anchor='center') #hace que el texto esté en el centro

'canción'
pygame.init()   #inicia pygame
muted = False   #variable para mutear
volumen_actual = 0.1    #volumen
def music():    #función para canción principal
    pygame.mixer.init()        #inicializa el mezclador de sonido de Pygame
    pygame.mixer.music.load('Archivos/menusong.mp3')  #ruta
    pygame.mixer.music.set_volume(volumen_actual)  #volumen
    pygame.mixer.music.play()   #play

music() #hace que se inicie music al correr

def mute():
    global muted, volumen_actual #global de muted y volumen
    if muted:
        pygame.mixer.music.set_volume(volumen_actual)   #crea la opción de muteado o no
        muted = False
    else:
        pygame.mixer.music.set_volume(0.0)
        muted = True


'Botones'
# Info
acerca = tk.Button(menu, width=4, height=1, text= 'Info', font=('Arial'), bg='white', fg='black', border=4, command=lambda:info()) #botón para info con tamaño, texto y borde
acerca.place(relx=0.9, rely=0.9) #ubicación
#set nickname
nick = tk.Button(menu, text='Set nickname', font=('Arial', 8), bg='white', fg='black', command='usuario') #botón para nick con texto y borde
nick.place(relx=0.627, rely=0.334, anchor='center') #ubicación
#parar canción
stop = tk.Button(menu, text='🔇', font=10, bg='white', fg='black', command=mute) #parar música con texto, colores
stop.place(relx=0.1, rely=0.9)
#Puntuaciones
score = tk.Button(menu, text='Puntuaciones',font=10, bg='white', fg='black') #botón puntuaciones
score.place(relx=0.5, rely=0.919, anchor='center')

'entradas'
nickname = tk.Entry(menu, font=('arial', 12), bg='#8B9FC2', fg='black', textvariable='data')
nickname.place(relx=0.359, rely=0.32)


#-------------------Ventana Juego------------------------------------------------#
gamefondo = PhotoImage(file='Archivos/juego.png')   #cargar imagen


tiempo_animacion = 2 #tiempo para los .after
velocidad = 5 #velocidad de la nave

"direcciones"
move_up = False
move_down = False
move_left = False
move_right = False


"Balas"
bala_lanzada = False #verifica si se lanzó una bala
last_bullet_time = 0 #tiempo para la siguiente bala
bala = None         #balas


"vida y puntuación"
vida = 3
puntuacion = tk.IntVar(value=0)


"luv para bucle loop"
luv = True

enemigos_creados = 0

"pantalla de info"
def info():
    venID = tkinter.Toplevel()
    venID.title("Ficha Personal")
    venID.minsize(1000, 709)
    venID.maxsize(1000, 709)

    # canva para id
    canvaid = tkinter.Canvas(venID, width=1000, height=709, borderwidth=0, highlightthickness=0, bg="white")
    canvaid.place(x=0, y=0, anchor=NW)

    ITCR = tkinter.Label(venID, text='Instituto Tecnológico de costa rica', bg='white', fg='black', font=('Arial', 15))
    ITCR.place(x= 370, y=3)

    nombre = tkinter.Label(venID, text='Harold Madriz Cerdas', bg='white', fg='black', font=('Arial', 12))
    nombre.place(x=2, y=400)

    C = tkinter.Label(venID, text='Cédula:305470792', bg='white', fg='black', font=('Arial', 12))
    C.place(x=2, y=420)

    año = tkinter.Label(venID, text='2023', bg='white', fg='black', font=('Arial', 12))
    año.place(x=940, y=660)

    profesor = tkinter.Label(venID, text='Profesor: Jeff Schmidt Peralta', bg='white', fg='black', font=('Arial', 12))
    profesor.place(x=2, y=440)

    ce = tkinter.Label(venID, text='Ingeniería en Computadores', bg='white', fg='black', font=('Arial', 12))
    ce.place(x=2, y=460)

    asig = tkinter.Label(venID, text='Taller de Programación', bg='white', fg='black', font=('Arial', 12))
    asig.place(x=2, y=480)

    CR = tkinter.Label(venID, text='Costa Rica', bg='white', fg='black', font=('Arial', 12))
    CR.place(x=2, y=600)

    ver = tkinter.Label(venID, text='Python 3.11', bg='white', fg='black', font=('Arial', 12))
    ver.place(x=895, y=640)




def juego():
    global gamefondo, luv, puntuacion, enemigos_creados
    enemigos_creados = 0
    puntuacion.set(0)
    luv = True
    'Ventana'
    game = tk.Toplevel()
    game.wm_title("Space Impact")  # título
    game.maxsize(width=1280, height=720)  # para que no se mueva la ventana
    game.minsize(width=1280, height=720)

    ven.withdraw()#minimiza la ventana principal

    pygame.mixer.music.stop()#quita la música del menú

    # Vincular la función para volver a activar la ventana principal al evento WM_DELETE_WINDOW
    game.protocol("WM_DELETE_WINDOW", lambda:venmain(game))


    'Canva'
    plano = Canvas(game, bg='black', width=gamefondo.width(), height=gamefondo.height(), highlightthickness=0)
    plano.pack(fill='both', anchor=NW)

    'imagen para el juego'
    plano.create_image(0, 0, image=gamefondo, anchor=NW, tags='gamefondo')  # poner la imagen en el canvas


    
    'puntuación'
    fuentescore = tkinter.font.Font(family="Fixedsys", size=18) #fuente para el texto
    puntuaciones = tk.Label(plano, textvariable=puntuacion, font=fuentescore, bg='black', fg='white') #Label de puntuacion
    puntuaciones.place(x=1100, y=20)  #ubicacion

    'Nave'
    nave = cargarimg('nave.png')
    nave_imagen = plano.create_image(100, 200, image=nave, anchor=NW)#nave aliada
    side = plano.bbox(nave_imagen)#bbox de la nave


    'indicador de vida'
    corazonimg = cargarimg('vida.png')
    cora1 = plano.create_image(50, 60, image=corazonimg)  #corazones en pantalla
    cora2 = plano.create_image(80, 60, image=corazonimg)
    cora3 = plano.create_image(110, 60, image=corazonimg)

    'enemigos'
    enemyimg = cargarimg('enemy.png')       #enemigo, enemigo2 y boss
    enemy2img = cargarimg('enemy2.png')
    bossimg = cargarimg('boss.png')

    def loop():
        global puntuacion
        'funciones de direcciones'
        plano.bind_all('<KeyPress-w>', lambda event: mov('w'))  #w arriba
        plano.bind_all('<KeyPress-a>', lambda event: mov('a'))  #a izquierda
        plano.bind_all('<KeyPress-s>', lambda event: mov('s'))  #s abajo
        plano.bind_all('<KeyPress-d>', lambda event: mov('d'))  #d derecha


        plano.bind_all("<KeyPress-space>", lambda event: create_bullet()) #space disparo


        "función de movimiento"
        def mov(event):
            global move_up, move_right, move_left, move_down
            if event == 'w':
                move_up = True
                threading.Thread(target=up()).start()       #llama la función de arriba
            if event == 'a':
                move_left = True
                threading.Thread(target=left()).start()         #llama la fuición de izquierda
            if event == 's':
                move_down = True
                threading.Thread(target=down()).start()         #llama la fuición de abajo
            if event == 'd':
                move_right = True
                threading.Thread(target=right()).start()        #llama la fuición de derecha


        def up():
            global move_up, velocidad, tiempo_animacion         #variables globales
            side = plano.bbox(nave_imagen)          #bbox
            if side != None:  #si se elimina la nave no ocurre la función
                x1, y1, x2, y2 = side
                if y1 <= 0:     #límite de movimiento
                    move_up = False
                else:
                    plano.move(nave_imagen, 0, -velocidad) #movimiento
                    game.update() #actualiza la ventana
                    time.sleep(0.01) #tiempo de espera para que no acelere de más
                    game.after(tiempo_animacion, up if move_up else None) #repetición de ka función si la tecla está presionada

        def left():
            global move_left, velocidad, tiempo_animacion           #variables globales
            side = plano.bbox(nave_imagen)          #bbox
            if side != None:    #si se elimina la nave no ocurre la función
                x1, y1, x2, y2 = side
                if x1 <= 0:     #límite de movimiento
                    move_left = False
                else:
                    plano.move(nave_imagen, -velocidad, 0) #movimiento
                    game.update() #actualiza la ventana
                    time.sleep(0.01) #tiempo de espera para que no acelere de más
                    game.after(tiempo_animacion, left if move_left else None) #repetición de ka función si la tecla está presionada

        def down():
            global move_down, velocidad, tiempo_animacion       #variables globales
            side = plano.bbox(nave_imagen)              #bbox
            if side != None:    #si se elimina la nave no ocurre la función
                x1, y1, x2, y2 = side
                if y2 >= 720:       #límite de movimiento
                    move_down = False
                else:
                    plano.move(nave_imagen, 0, velocidad) #movimiento
                    game.update() #actualiza la ventana
                    time.sleep(0.01) #tiempo de espera para que no acelere de más
                    game.after(tiempo_animacion, down if move_down else None) #repetición de ka función si la tecla está presionada

        def right():
            global move_right, velocidad, tiempo_animacion          #variables globales
            side = plano.bbox(nave_imagen)          #bbox
            if side != None:    #si se elimina la nave no ocurre la función
                x1, y1, x2, y2 = side
                if x2 >= 1280:      #límite de movimiento
                    move_right = False
                else:
                    plano.move(nave_imagen, velocidad, 0) #movimiento
                    game.update() #actualiza la ventana
                    time.sleep(0.01) #tiempo de espera para que no acelere de más
                    game.after(tiempo_animacion, right if move_right else None) #repetición de ka función si la tecla está presionada

        def stop_up(event):
            global move_up
            move_up = False #si se suelta la tecla para el movimiento

        def stop_left(event):
            global move_left
            move_left = False #si se suelta la tecla para el movimiento

        def stop_down(event):
            global move_down
            move_down = False #si se suelta la tecla para el movimiento

        def stop_right(event):
            global move_right
            move_right = False #si se suelta la tecla para el movimiento


        #teclas para mandar a los stops y que pare el movimiento
        plano.bind('<KeyRelease-w>', stop_up)
        plano.bind('<KeyRelease-a>', stop_left)
        plano.bind('<KeyRelease-s>', stop_down)
        plano.bind('<KeyRelease-d>', stop_right)




        #actualiza los corazones de la vida
        if vida == 2:
            plano.delete(cora3)
        if vida == 1:
            plano.delete(cora2)
        if vida == 0:
            plano.delete(cora1)






        'balas'
        def create_bullet():
            global bala_lanzada, last_bullet_time, bala
            if bala_lanzada == False and time.time() - last_bullet_time > 0.5:  #verifica que no se haya lanzado una bala para no mandar otra seguidamente
                pium()     #sonido
                bala = plano.create_rectangle(0, 0, 20, 5, fill='red')  #rectánfulo de bala
                coorder = plano.bbox(nave_imagen)       #bbox bala
                if coorder != None:     # si la bbox es diferente de None continúa
                    s1, c1, s2, c2 = coorder
                    plano.move(bala, s2, c2-19)
                    moverbala(bala)
                    bala_lanzada = True
                    last_bullet_time = time.time()
                    bala_lanzada = False

        def moverbala(bala):
            plano.move(bala, 6, 0) #mueve la bala
            game.after(10, moverbala, bala) #repite


        if vida == 0:
            plano.delete(nave_imagen)   #si la vida es 0 borra la nave
        if luv == True:
            game.after(5, loop)




        def pium():
            pygame.mixer.init()  # inicializa el mezclador de sonido de Pygame
            pygame.mixer.music.load('Archivos/disparo.mp3')  # ruta
            pygame.mixer.music.set_volume(volumen_actual)  # volumen
            pygame.mixer.music.play()


        "Dificultades"
        def easy():     #fácil
            global enemigos_creados
            if enemigos_creados < 13: #crea enemigos hasta que la global enemigos_creados llega a 13
                create_enemy()
                enemigos_creados += 1

        def medium(): #medio
            global enemigos_creados
            if enemigos_creados < 25: #crea enemigos hasta que la global enemigos_creados llega a 25
                create_enemy2()
                enemigos_creados += 1

        def hard(): #difícil
            global enemigos_creados
            enemigos_creados += 1
            if enemigos_creados == 26:  #crea el boss
                create_boss()
                enemigos_creados += 1




        def create_enemy():
            enemy = plano.create_image(random.randint(1280, 2000), random.randint(0, 720), image=enemyimg) #crea el enemigo básico
            moveattack(enemy, 1) #lo manda a moverse
            move_enemy(enemy, plano.bbox(enemy)) # hace que se mueva en el eje y de vez en cuando
            dis = random.choice([True, False]) #hace que algunos disparen y otros no
            if dis:
                bullet_enemy(enemy)

        def create_enemy2():
            enemy2 = plano.create_image(random.randint(1280, 2000), random.randint(0, 720), image=enemy2img) #crea el enemigo fuerte
            moveattack(enemy2, 3) #lo manda a moverse
            dis = random.choice([True, False]) #hace que algunos disparen y otros no
            if dis:
                bullet_enemy(enemy2)

        def create_boss():
            boss = plano.create_image(1300, 360, image=bossimg) #crea el boss
            moveboss(boss, 20) #lo manda a moverse
            bossattack(boss)  #hace que genere naves

        def moveboss(boss, health): #moviemiento y vida del boss
            if boss != None:        #si el boss no es None continúa
                # Obtener las coordenadas actuales del boss utilizando bbox
                bbox = plano.bbox(boss) #bbox del boss
                if bbox is not None:     # si la bbox es diferente de None continúa
                    x1, y1, x2, y2 = bbox #desempaca la bbox
                    overlapping = plano.find_overlapping(x1, y1, x2, y2) #crea un overlapping de la bbox
                if bala in overlapping:
                    plano.delete(bala)  #si la bala está en overlapping, quita vida, elimina la bala y ejecuta el sonido
                    health -= 1
                    destroy_enemy()
                    if health <= 0:     #si la vida es 0 o menor elimina el boss y suma la puntuación
                        plano.delete(boss)
                        puntuacion.set(puntuacion.get() + 50)
                    else:
                        # El boss todavía tiene salud, moverlo de manera aleatoria
                        plano.move(boss, random.randint(-10, 10), random.randint(-10, 10))
                        game.after(100, moveboss, boss, health)
                else:
                    # No hay colisión con la bala, mover el boss hacia la derecha
                    if x1 <= 640:
                        plano.move(boss, random.randint(40, 300), 0)
                    else:
                        # El boss ha alcanzado el borde derecho de la pantalla
                        plano.move(boss, random.randint(-10, 10), random.randint(-10, 10))
                    game.after(100, moveboss, boss, health)



        def moveattack(enemy, health): #movimiento y vida de enemigos
            global puntuacion #global de puntuación
            if enemy != None:   #si el enemy no es None continúa
                bbox = plano.bbox(enemy) #bbox del enemy
                if bbox != None:  # si la bbox es diferente de None continúa
                    m1, n1, m2, n2 = bbox #desempaca la bbox
                    if m2 < -30:            # si el enemigo llega a -30 en x vueve a aparecer en el otro lado de la pantalla
                        plano.coords(enemy, (random.randint(1280, 1400)), (random.randint(0, 720)))
                        game.after(10, moveattack, enemy, health)
                    else:
                        verificar_colision(enemy, nave_imagen)  #verifica la colisión de la nave y el enemy
                        overlapping = plano.find_overlapping(*bbox)
                        if bala in overlapping:             #overlapping de bala y enemy
                            health -= 1         #resta vida
                            destroy_enemy()  # sonido
                            if health < 1:          #si la vida es 0 borra el enemigo y suma puntuación
                                plano.delete(enemy)
                                puntuacion.set(puntuacion.get() + 1)
                            else:
                                plano.move(enemy, -1, 0)
                                game.after(100, moveattack, enemy, health)  #si nña vida no es 0 continúa
                        else:
                            plano.move(enemy, -1, 0)
                            game.after(10, moveattack, enemy, health) #si no colisiona continúa moviéndose





        def move_enemy(enemy, bbox):
            if enemy != None:   #si el enemy no es None continúa
                bbox = plano.bbox(enemy) #bbox del enemy
                if bbox != None:   # si la bbox es diferente de None continúa
                    t1, r1, t2, r2 = bbox #desempaca la bbox
                    if r1 <= 0:     #evita que se salga del borde la pantalla
                        plano.move(enemy, 0, random.randint(40, 90))
                        game.after(4000, move_enemy, enemy, bbox)
                    else:
                        if r2 >= 721:       #evita que se salga del borde la pantalla
                            plano.move(enemy, 0, random.randint(-90, -40))
                            game.after(4000, move_enemy, enemy, bbox)
                        else:
                            plano.move(enemy, 0, random.randint(-40, 40))       #movimiento normal
                            game.after(4000, move_enemy, enemy, bbox)

        def moverbalaenemy(bala):
            if bala != None:   #si el enemy no es None continúa
                verificar_colision(bala, nave_imagen) #manda a verificar la colisión con la nave
                balabox = plano.bbox(bala)
                if balabox != None:
                    h1, k1, h2, k2 = balabox
                    if h2 <= -25:
                        plano.delete(bala)  #si la bala está en -25 se elimina
                    else:
                        plano.move(bala, -10, 0) #mueve la bala
                        game.after(15, moverbalaenemy, bala) #continúa el movimiento





        def bullet_enemy(enemy):
            aveces = random.randint(1, 100000)
            if enemy != None and plano.find_withtag(enemy):
                if aveces % 2 == 0 and aveces > 50:
                    piumenemy()
                    balaenemy = plano.create_rectangle(0, 0, 20, 5, fill='green')
                    coorder = plano.bbox(enemy)
                    if coorder is not None:
                        s1, c1, s2, c2 = coorder
                        plano.move(balaenemy, s1, c1 + 35)
                        moverbalaenemy(balaenemy)
                        game.after(random.randint(500, 1000), bullet_enemy, enemy)
                else:
                    game.after(5000, bullet_enemy, enemy)

        def bossattack(boss):
            aveces = random.randint(1, 100000)
            if boss != None:
                if aveces % 2 == 0 and aveces > 1000:
                    piumenemy()
                    dis = random.choice([False, True])
                    if dis == True:
                        create_enemy()
                        game.after((random.randint(500, 1000)), bossattack, boss)
                    else:
                        create_enemy2()
                        game.after((random.randint(500, 1000)), bossattack, boss)
                else:
                    game.after(7000, bossattack, boss)




        #Dificultades, 3 niveles dependiendo de la puntuación
        if puntuacion.get() < 10:
            easy()
        if puntuacion.get() >= 10 and puntuacion.get() < 21:
            medium()
        if puntuacion.get() >= 22:
            hard()



    def piumenemy():
        pygame.mixer.init()  # inicia el mezclador de sonido de Pygame
        pygame.mixer.music.load('Archivos/disparoenemy.mp3')  # ruta
        pygame.mixer.music.set_volume(volumen_actual)  # volumen
        pygame.mixer.music.play()

    def damage():
        pygame.mixer.init()  # inicia el mezclador de sonido de Pygame
        pygame.mixer.music.load('Archivos/damage.mp3')  # ruta
        pygame.mixer.music.set_volume(volumen_actual)  # volumen
        pygame.mixer.music.play()


    def destroy_enemy():
        pygame.mixer.init()  # inicia el mezclador de sonido de Pygame
        pygame.mixer.music.load('Archivos/desenemy.mp3')  # ruta
        pygame.mixer.music.set_volume(volumen_actual)  # volumen
        pygame.mixer.music.play()


    def verificar_colision(objeto1, objeto2):
        global vida
        # Obtener las coordenadas de los rectángulos que representan los objetos
        if objeto1 != None and objeto2 != None:
            bbox2 = plano.bbox(objeto2)
            if bbox2 != None:
                overlapping = plano.find_overlapping(*bbox2)
                if objeto1 in overlapping:
                    damage()
                    vida -= 1
                    plano.delete(objeto1)







    plano.focus_set()
    loop()
    game.mainloop()


def venmain(game):
    global luv
    game.destroy()
    ven.deiconify()
    music()
    luv = False


'Botón en ventana principal para play'
play = tk.Button(menu, text='Play', font=FuenteMenu, bg='#1A2E50', fg='white', border=5, command=lambda:juego())   #botón para play con texto y borde
play.place(relx=0.5, rely=0.4, anchor='center') #ubicación



ven.mainloop()