### CLAVE MAJO###

import random
import time
import msvcrt

intentos=0 #Variable contante de intentos

MENSAJES_ERROR = [  #Arreglo mensajes de error
    "Clave incorrecta. Te quedan 2 intentos.",
    "Clave incorrecta. Te queda 1 intento.",
    "Clave incorrecta. No te quedan intentos. Sesion bloqueada."
]

#FUNCION QUE GENERA CLAVE 
def generar_clave():
    numero=random.randint(100000,999999)
    clave=str(numero)
    return clave

def verificar_clave(clave): 
    global intentos
    if len(clave)!=6:
        return False
    intentos+=1
    if intentos<=len(MENSAJES_ERROR):
        print(f"   {MENSAJES_ERROR[intentos - 1]}")
    return False


###### temporizador#####
def temporizador(timer,contraseña,nombre):
    Frases=["Empezando. Tu guardian tiene la clave","Buen comienzo! Ya completaste el 25%.","A la mitad! Sigue asi.","Casi listo! Solo falta el 25%.","Ultimo tramo! No pares ahora.","Sesion completada. Excelente trabajo!"]
    inicio=timer
    print("\nPresiona 'ESC' para salir e ingresar contraseña...")
    intentos=0

    while timer>=0:
        #cuantos minutos
        min=timer//60
        #cuantos segundos
        sec=timer-(min*60)
        #longitud barra y funcionamiento
        longitud=25
        progreso=(inicio-timer)/ inicio 
        llenado=int(longitud*progreso)
        barra="█"*llenado +"-"*(longitud-llenado)
        porcentaje=progreso*100

        #Frases de motivacion en cada momento de la sesion
        if porcentaje==0 :
            print(f"\r{Frases[0]}                                        ")
        elif porcentaje==25:
           print(f"\r{Frases[1]}                                         ") 
        elif porcentaje==50:
           print(f"\r{Frases[2]}                                         ") 
        elif porcentaje==75:
           print(f"\r{Frases[3]}                                         ") 
        elif porcentaje==90:
           print(f"\r{Frases[4]}                                         ") 
        elif porcentaje==100:
           print(f"\r{Frases[5]}                                         ") 
        
        #Muesta progreso
        #procentaje: 3. largo total del numero inncluyendo punto y decimal, 1: numeros de decimales, f:float
        #flush=true : sirve para que se muestre el progreso y no se muestre ya cuando la barra este al 100,
        print(f"\rProgreso: |{barra}| {porcentaje:3.1f}% - Faltan: {min:02d}:{sec:02d}", end='', flush=True)
        for _ in range(10):
            if intentos<3:
                if msvcrt.kbhit():
                    tecla = msvcrt.getch()
                    if tecla == b'\x1b':
                        print("\n\n[SISTEMA BLOQUEADO] Intento de salida detectado.")
                        clave = input("Introduce la contraseña para salir: ")
                        if clave == contraseña:
                            print("Contraseña correcta. Sesión terminada.")
                            penalizacion(nombre)
                            return
                        else:
                            verificar_clave(clave)
        
            time.sleep(0.1) 
            
        timer -= 1
    print("\n\nTiempo agotado!")
    return True




#####Puntos###########
#matriz que va aumentando

#matriz con niveles dependiendo de cantidad de puntos
niveles = [
    ["Novato",      0,    99,   "🌱"],
    ["Aprendiz",    100,  299,  "📚"],
    ["Enfocado",    300,  599,  "🎯"],
    ["Avanzado",    600,  999,  "⚡"],
    ["Experto",     1000, 1999, "🔥"],
    ["Maestro",     2000, 9999, "👑"]
]

#matriz con pos 1: tiempo, pos 2: puntos y pos 3: bonus si tiene racha
tabla_puntos = [
    [25,  20,  5],  
    [50,  45,  10],
    [90,  80,  20],
    [120, 120, 30]
]

#mensajes por racha
Mmensajes_racha = [
    [1,  "Buen inicio de racha!"],
    [3,  "3 dias seguidos. Vas bien!"],
    [7,  "Una semana completa. Increible!"],
    [14, "Dos semanas sin parar. Leyenda!"],
    [30, "Un mes completo. Eres un Maestro!"]
]

#puntos , retorna total puntos
def puntos(sec,nombre):
    indice=buscar_usuario(nombre)
    if indice==-1:
        return 0
    puntos_actuales = matrizdataUsuarios[indice][1]
    racha_actual = matrizdataUsuarios[indice][2]
    #puntos por sesiones completadas
    match sec:
        case 1500:
            puntos_base = 1400
        case 3000:
            puntos_base = 2800
        case 5400:
            puntos_base = 5200
        case 7200: 
            puntos_base = 7000
        case _:
            puntos_base = sec-5

    matrizdataUsuarios[indice][1]+= puntos_base
    matrizdataUsuarios[indice][2]+= 1
    matrizdataUsuarios[indice][3] += 1


    print(f"\n   Puntos base:    +{puntos_base}")
    print(f"   Total acumulado: {matrizdataUsuarios[indice][1]}")
    print(f"   Racha actual:    {matrizdataUsuarios[indice][2]} dias")   
 


def penalizacion(nombre):
    indice = buscar_usuario(nombre)
    if indice == -1:
        return 0

    puntos_actuales = matrizdataUsuarios[indice][1]
    penalizacion = puntos_actuales // 10

    if penalizacion < 10: 
        penalizacion = 10
    if penalizacion > 50:
        penalizacion= 50

    if penalizacion > puntos_actuales:
        penalizacion = puntos_actuales

    matrizdataUsuarios[indice][1] -=penalizacion

    matrizdataUsuarios[indice][2]=0
    matrizdataUsuarios[indice][4]+=1

    print(f"\n   Penalizacion:    -{penalizacion} puntos")
    print(f"   Puntos totales:  {matrizdataUsuarios[indice][1]}")
    print(f"   Racha reiniciada a 0.")                             


def nivel_actual(nombre): 
    indice = buscar_usuario(nombre)
    puntos_u = matrizdataUsuarios[indice][1]
    if indice != -1:
        puntos_u = matrizdataUsuarios[indice][1]  # Si existe, toma sus puntos reales
    else:
        puntos_u = 0                              # Si no existe, ponle 0 puntos
    nivel_encontrado = niveles[0]

    for fila in niveles:
        if puntos_u >= fila[1] and puntos_u <= fila[2]:
            nivel_encontrado = fila
            break
    return nivel_encontrado


def nivel(nombre):
    indice = buscar_usuario(nombre)
    if indice == -1: 
        return
    puntos_u = matrizdataUsuarios[indice][1]
    nivel = nivel_actual(nombre)
    nombre_nivel = nivel[0]
    pts_max = nivel[2]
    emoji = nivel[3]

    falta = pts_max - puntos_u

    print(f"\n   {emoji} Nivel actual: {nombre_nivel}")
    print(f"   Puntos: {puntos_u} | Faltan {falta} para el siguiente nivel")



def mensaje_racha(racha):
    mensaje_actual = ""
    for item in Mmensajes_racha: 
        if racha >= item[0]:
            mensaje_actual = item[1]
    if mensaje_actual != "":
        print(f"  {mensaje_actual}")

#####usuarioo####

#Matriz de usuarios registrados.
#  Usuarios, puntos, racha, sesiones_ok, sesiones_fallo
matrizdataUsuarios=[
    ["Maria P", 120, 9, 14, 2],
    ["Andres", 0, 0, 0, 0 ],
    ["Valeria", 280, 5, 9, 3],
    ["Camilo", 195, 3, 7 , 4],
    ["Maria J", 120, 1, 4, 5]]

def buscar_usuario(nombre):
    for i in range(len(matrizdataUsuarios)):
        nombreUsuario= matrizdataUsuarios[i][0]
        if nombreUsuario.lower()==nombre.lower():
            return i
        
    return -1


def registro_nuevo_usuario(nombre, puntos, racha, sesiones_ok,sesiones_fallo):
    nuevo_usuario=[nombre,puntos, racha, sesiones_ok,sesiones_fallo]
    matrizdataUsuarios.append(nuevo_usuario)

def mostrar_perfil(nombre):
    indice=buscar_usuario(nombre)
    if indice==-1:
        print(f"Usuario {nombre} no encontrado")
        return -1
    
    NombreU= matrizdataUsuarios[indice][0] #Usuario
    PuntosU= matrizdataUsuarios[indice][1] #Puntos
    RachaU= matrizdataUsuarios[indice][2] #Racha
    SesionesOkU= matrizdataUsuarios[indice][3] #SesionesOk
    SesionesFallidasU= matrizdataUsuarios[indice][4] #SesionesFallidas

    #Calculo de la tasa de exito
    totalSesiones= SesionesOkU+SesionesFallidasU
    if totalSesiones>0:
        tasa=(SesionesOkU/totalSesiones)*100 
    else:
        tasa=0.0
    #promedio local usuario
    #Mirar
    totalpuntos = 0
    ContadorSesiones = 0
    promedio = round(totalpuntos / ContadorSesiones, 1) if ContadorSesiones > 0 else 0.0

    #Mostrar al usuario
    nivel = nivel_actual(nombre)

    print("\n" + "=" * 42)  
    print("   RESUMEN DE PUNTOS")
    print("=" * 42)
    print(f"   Nivel:              {nivel[3]} {nivel[0]}")
    print(f"   Puntos totales:     {PuntosU}")
    print(f"   Racha actual:       {RachaU} dias")
    print(f"   Sesiones ok:        {SesionesOkU}")
    print(f"   Sesiones fallidas:  {SesionesFallidasU}")
    print(f"   Promedio puntos:    {promedio}")
    print(f"   Tasa de exito:      {tasa:3.1f}%")
    print("=" * 42)


def ranking():
    matrizRanking =list(matrizdataUsuarios)
    n=len(matrizRanking)
    for i in range(n):
        for j in range(0,n-i-1):
            if matrizRanking[j][1]< matrizRanking[j+1][1]:
                matrizRanking[j], matrizRanking[j+1] = matrizRanking[j+1], matrizRanking[j]

    print("Ranking final ")
    for fila in matrizRanking:
        print(f"Nombre: {fila[0]: <12} Puntos: {fila[1]}")




###### menuuuuu#########


# Arreglo con las opciones del menu principal
OPCIONES_MENU= [
    "1. Iniciar sesion de enfoque",
    "2. Ver ranking semanal",
    "3. Ver mi perfil",
    "4. Cambiar usuario",
    "5. Ver tabla",
    "6. Salir"
]



#Imprime el menu principal con el nombre del usuario
def mostrar_menu(nombre):
    indice=buscar_usuario(nombre)
    print("\n" + "=" * 42)
    print("   GRINDLOCK - Sin distracciones.")
    print("=" * 42)
    if indice!=-1:
        print(f"   Usuario actual: {matrizdataUsuarios[indice][0]}")
        print(f"   Sesiones completadas: {matrizdataUsuarios[indice][3]}")
    print("=" * 42)

    # FOR: recorre el arreglo de opciones para mostrarlas
    for opcion in OPCIONES_MENU:
        print(f"   {opcion}")

    print("=" * 42)


#Funcion principal: el WHILE que mantiene el programa vivo.

##MatrizDataUsuarios 
print("\n" + "=" * 42)
print("   Bienvenido a GRINDLOCK")
print("=" * 42)
print(f"{'USUARIO':<12} {'PUNTOS':<12} {'RACHA':<12} {'SES. OK':<12} {'SES. FALLO':<12}")

for i in range(len(matrizdataUsuarios)):
    for j in range(len(matrizdataUsuarios[i])):
        print(f"{matrizdataUsuarios[i][j]:<12}", end=" ")
    print()
print("="*42)

print("INICIAR SESION")
nombre=input("Escriba el nombre del usuario:  ")
if buscar_usuario(nombre) == -1:
    print("Usuario no encontrado")
    print()
    registro=input("Desea ingresar un nuevo usuario Si/No: ")
    if registro=="Si" or registro=="si":
        registro_nuevo_usuario(nombre,0,0,0,0)
        print(f"Registro exitoso {nombre}")
    else:
        print("Deacuerdo, no se hara registro ")


activo= True                             # Variable de control del WHILE

    # WHILE principal - se repite hasta que el usuario elija salir
while activo:
    mostrar_menu(nombre)
    opcion=int(input("Elige tu opcion: "))
    menu=0
        # SWITCH / MATCH / CASE - una rama por opcion
    match opcion:
        case 1:
             while menu!=6:
                print("=====SESIONES=====")
                guardian=input("Escribe el nombre de tu guardian: ")
                menu=int(input("Cuantos minutos quiere estar concentrado\n  1. 25 min (+20 pts)\n  2. 50 min (+45 pts)\n  3. 90 min (+80 pts)\n  4. 120 min (+120 pts)\n  5.Personalizar\n  6.Salir\n"))

#menu con todas las opciones del temporizador dependiendo de lo que escoge el usuario, se rescriben las variables para la funcion temporizador 
                match menu:
                    case 1:
                        timer=1500
                        contraseña=generar_clave()
                        print(contraseña)
                        acabo = temporizador(timer, contraseña, nombre)
                        if acabo==True:
                            points=puntos(timer,nombre)
                        print("="*42)
                        opcion=input("          QUIERES SEGUIR ESTUDIANDO?:Si/No \n")
                        if opcion=="No" or opcion=="no":
                            menu=6                       
                    case 2:
                        timer=3000
                        contraseña=generar_clave()
                        acabo = temporizador(timer, contraseña, nombre)
                        if acabo==True:
                            points=puntos(timer, nombre)
                        print("="*42)
                        opcion=input("          QUIERES SEGUIR ESTUDIANDO?:Si/No \n")
                        if opcion=="No" or opcion=="no":
                            menu=6
                    case 3:
                        timer=5400
                        contraseña=generar_clave()
                        acabo = temporizador(time, contraseña, nombre)
                        if acabo==True:
                            points=puntos(timer)
                        print("="*42)
                        opcion=input("          QUIERES SEGUIR ESTUDIANDO?:Si/No \n")
                        if opcion=="No" or opcion=="no":
                            menu=6
                    case 4:
                        timer=7200
                        contraseña=generar_clave()
                        acabo = temporizador(timer, contraseña, nombre)
                        if acabo==True:
                            points=puntos(timer, nombre)
                        print("="*42)
                        opcion=input("          QUIERES SEGUIR ESTUDIANDO?:Si/No \n")
                        if opcion=="No" or opcion=="no":
                            menu=6
                    case 5:
                        min=int(input("Cuantos minutos quiere estar concentrado?: "))
                        sec=int(input("Cuantos segundos?: "))
                        timer=min*60+sec
                        contraseña=generar_clave()
                        print(contraseña)
                        acabo = temporizador(timer, contraseña, nombre)
                        if acabo:
                            points = puntos(timer, nombre)
                        print("="*42)
                        opcion=input("          QUIERES SEGUIR ESTUDIANDO?:Si/No \n")
                        if opcion=="No" or opcion=="no":
                            menu=6
                    case 6:
                        print("Hasta la próxima")
                    case _:
                        print("Opcion invalida. Vuelva a intentarlo")

        case 2:
            ranking()
        case 3:
            lol=int(input("Quieres ver un resumen o ver tu nivel?: \n  1.Resumen\n  2.Nivel\n"))
            match lol:
                case 1:
                    mostrar_perfil(nombre)
                case 2:
                    nivel(nombre)
                case _:
                    print("Opcion invalida, vuelve a intentar")
        case 4:
            nombre=input("Escriba el nombre del usuario: ")
            if buscar_usuario(nombre) == -1:
                print("Usuario no encontrado")
                print()
                registro=input("Desea ingresar un nuevo usuario Si/No: ")
                if registro=="Si" or registro=="si":
                    registro_nuevo_usuario(nombre,0,0,0,0)
                    print(f"Deacuerdo bienvenido {nombre}")
                mostrar=input("Desea ver la matriz de usuarios Si/No \n Opcion: ")
                if mostrar=="Si"or mostrar=="si":
                    print(f"{'USUARIO':<12} {'PUNTOS':<12} {'RACHA':<12} {'SES. OK':<12} {'SES. FALLO':<12}")
                    for i in range(len(matrizdataUsuarios)):
                        for j in range(len(matrizdataUsuarios[i])):
                            print(f"{matrizdataUsuarios[i][j]:<12}", end=" ")
                        print()
                    print("="*42)

            elif buscar_usuario(nombre)!=-1:
                print(f"Deacuerdo bienvenido {nombre}")
                mostrar=input("Desea ver la matriz de usuarios Si/No \n Opcion: ")
                if mostrar=="Si"or mostrar=="si":
                    print(f"{'USUARIO':<12} {'PUNTOS':<12} {'RACHA':<12} {'SES. OK':<12} {'SES. FALLO':<12}")
                    for i in range(len(matrizdataUsuarios)):
                        for j in range(len(matrizdataUsuarios[i])):
                            print(f"{matrizdataUsuarios[i][j]:<12}", end=" ")
                        print()
                    print("="*42)
        case 5:
            print(f"{'USUARIO':<12} {'PUNTOS':<12} {'RACHA':<12} {'SES. OK':<12} {'SES. FALLO':<12}")
            for i in range(len(matrizdataUsuarios)):
                for j in range(len(matrizdataUsuarios[i])):
                    print(f"{matrizdataUsuarios[i][j]:<12}", end=" ")
                print()
            print("="*42)

                
        case 6:
            activo = False                      # Sale del WHILE
            print("\n   Hasta la proxima sesion. Sigue enfocado!")
        case _:
            print("   Opcion invalida. Intenta de nuevo.")