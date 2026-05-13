### CLAVE MAJO###

import random
import time
import msvcrt
hola="x"
clave_activa = ""     # Clave que se genera en cada sesión
tiempo_fin = 0.0    # Tiempo cuando se termina la sesión
intentos= 0      # Contador del número de intentos que lleva el usuario ingresando la clave.
MAX_INTENTOS= 3      # Límite de intentos permitidos -> Constante
guardian_actual= ""     # Nombre del amigo guardián

historial_claves=[]       # Matriz que guarda el historial de cada sesión: clave, tiempo, amigo guardián.

#Variable contante de intentos
MENSAJES_ERROR = [
    "Clave incorrecta. Te quedan 2 intentos.",
    "Clave incorrecta. Te queda 1 intento.",
    "Clave incorrecta. No te quedan intentos. Sesion bloqueada."
]

#FUNCION QUE GENERA CLAVE 
def generar_clave():
    numero=random.randint(100000,999999)
    clave=str(numero)
    return clave

def iniciar_sesion_clave(minutos, guardian):
    global clave_activa, tiempo_fin, intentos, guardian_actual

    clave_activa=generar_clave() # Genera una clave con la función para la sesion actual
    intentos = 0 # Reinicia el contador
    guardian_actual=guardian 

    registro: list =[clave_activa, minutos, guardian] # Guarda la clave de la sesión, los minutos, el nombre del guardián y la hora actual
    historial_claves.append(registro)
    
    return(clave_activa)


def verificar_clave(clave):
    global intentos
    if len(clave)!=6:
        return False
    intentos+=1
    if intentos<=len(MENSAJES_ERROR):
        print(f"   {MENSAJES_ERROR[intentos - 1]}")
    return False

#funcion que guarda toda la infromacion de las seciones anteriores
def mostrar_historial_claves():
    print("\n   Historial de sesiones:")
    print("   " + "-" * 36)
    if len(historial_claves)==0:
        print(" No hay sesiones registradas.")
        return
    else:
        for i in range (len(historial_claves)):
            sesion: list = historial_claves[i]
            clave_historial: int = sesion[0]
            minutos_historial: int = sesion[1]
            guardian_historial: str = sesion[2]
            print(f"   Sesion {i + 1}: {minutos_historial} min | Guardian: {guardian_historial}")

    print("   " + "-" * 36)

#funcion que dice el total de sesiones realizadas
def obtener_total_sesiones()->int:
    return(len(historial_claves))   

###### temporizador#####
def temporizador(timer,min,sec,contraseña):
    Frases=["Empezando. Tu guardian tiene la clave","Buen comienzo! Ya completaste el 25%.","A la mitad! Sigue asi.","Casi listo! Solo falta el 25%.","Ultimo tramo! No pares ahora.","Sesion completada. Excelente trabajo!"]
    inicio=timer
    print("\nPresiona 'ESC' para salir e ingresar contraseña...")
    intento=0
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
        if porcentaje>=0 and porcentaje<1:
            print(f"\r{Frases[0]}                                        ")
        elif porcentaje>=25 and porcentaje<26:
           print(f"\r{Frases[1]}                                         ") 
        elif porcentaje>=50 and porcentaje<=51:
           print(f"\r{Frases[2]}                                         ") 
        elif porcentaje>=75 and porcentaje<=76:
           print(f"\r{Frases[3]}                                         ") 
        elif porcentaje>=90 and porcentaje<=91:
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
                            penalizacion()
                            return
                        else:
                            verificar_clave(clave)
                            intento=intento+1
            time.sleep(0.1) 
            
        timer -= 1
    print("\n\nTiempo agotado!")
    return True






puntos_totales = 0
racha_actual = 0
racha_maxima = 0
sesiones_ok = 0
sesiones_fallo = 0

#matriz que va aumentando
historial_puntos = []

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
def puntos(sec):
    global puntos_totales, racha_actual, racha_maxima, sesiones_ok
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
    
    #bonus por racha 
    bonus_racha = 0
    for fila in tabla_puntos:                       
        if fila[0] == sec:                      
            if racha_actual >= 7:                   
                bonus_racha = fila[2] 

    total = puntos_base + bonus_racha

    puntos_totales = puntos_totales + total
    racha_actual += 1
    sesiones_ok += 1

    #racha maxima es la racha actual
    if racha_actual > racha_maxima:
        racha_maxima = racha_actual

    #.append: poner otro dato al final de historial_puntos
    historial_puntos.append([total, True, sec]) 

    print(f"\n   Puntos base:    +{puntos_base}")
    print(f"   Bonus racha:    +{bonus_racha}")
    print(f"   Total ganado:   +{total}")
    print(f"   Total acumulado: {puntos_totales}")
    print(f"   Racha actual:    {racha_actual} dias")

    mensaje_racha(racha_actual)   

    return total  


def penalizacion():
    global puntos_totales, racha_actual, sesiones_fallo

    penalizacion = puntos_totales // 10 

    if penalizacion < 10: 
        penalizacion = 10
    if penalizacion > 50:
        penalizacion= 50

    if penalizacion > puntos_totales:
        penalizacion = puntos_totales

    puntos_totales = puntos_totales - penalizacion
    racha_actual = 0
    sesiones_fallo += 1

    historial_puntos.append([-penalizacion, False, 0]) 

    print(f"\n   Penalizacion:    -{penalizacion} puntos")
    print(f"   Puntos totales:  {puntos_totales}")
    print(f"   Racha reiniciada a 0.")

    return penalizacion                             


def nivel_actual(): 
    nivel_encontrado = niveles[0]

    for fila in niveles: 
        pts_min = fila[1]
        pts_max = fila[2]

        if puntos_totales >= pts_min and puntos_totales <= pts_max:
            nivel_encontrado = fila
            break
    return nivel_encontrado


def nivel(puntos_nuevos):
    nivel = nivel_actual()
    nombre = nivel[0]
    pts_max = nivel[2]
    emoji = nivel[3]

    falta = pts_max - puntos_totales

    print(f"\n   {emoji} Nivel actual: {nombre}")
    print(f"   Puntos: {puntos_totales} | Faltan {falta} para el siguiente nivel")


def promedio_puntos(): 
    if len(historial_puntos) == 0: 
        return 0.0
    
    total_pts = 0
    sesiones_contadas = 0

    for entrada in historial_puntos:
        pts = entrada[0]
        existosa = entrada[1]

        if existosa and pts > 0:
            total_pts = total_pts + pts
            sesiones_contadas += 1

    if sesiones_contadas == 0:
        return 0.0
    
    promedio = total_pts / sesiones_contadas
    return round(promedio, 2) 

def tasa_exito():
    total = len(historial_puntos)
    if total == 0:
        return 0.0
    
    exitosas = 0
    for entrada in historial_puntos: 
        if entrada[1]:
            exitosas +=1
    
    tasa = (exitosas / total) * 100
    return round(tasa, 1)

def mensaje_racha(racha):
    mensaje_actual = ""
    for item in Mmensajes_racha: 
        umbral = item[0]
        mensaje = item[1]

        if racha >= umbral:
            mensaje_actual = mensaje

    if mensaje_actual != "":
        print(f"  {mensaje_actual}")    

def resumen_puntos():
    nivel = nivel_actual()

    print("\n" + "=" * 42)  
    print("   RESUMEN DE PUNTOS")
    print("=" * 42)
    print(f"   Nivel:            {nivel[3]} {nivel[0]}")
    print(f"   Puntos totales:   {puntos_totales}")
    print(f"   Racha actual:     {racha_actual} dias")
    print(f"   Racha maxima:     {racha_maxima} dias")
    print(f"   Sesiones ok:      {sesiones_ok}")
    print(f"   Sesiones fallidas:{sesiones_fallo}")
    print(f"   Promedio puntos:  {promedio_puntos()}")
    print(f"   Tasa de exito:    {tasa_exito()}%")
    print("=" * 42)





#####usuarioo####
print("\n" + "=" * 42)
print(" Modulo Usuarios ")

#Matriz de usuarios registrados.
#  Usuarios, puntos, racha, sesiones_ok, sesiones_fallo
matrizdataUsuarios=[
    ["Maria P", 120, 9, 14, 2],
    ["Andres", 0, 0, 0, 0 ],
    ["Valeria", 280, 5, 9, 3],
    ["Camilo", 195, 3, 7 , 4],
    ["Maria J", 120, 1, 4, 5]]
indice_Activo=1
#Usuario, minutos, puntos, exitosa True False
MatrizHistorialSesiones=[] #Matriz vacia que va a ir creciendo
#App, paquete Android, bloqueadaporDefault True False
MatrizAppsDisponibles=[["Instagram",  "com.instagram.android",        True],
                       ["TikTok",     "com.zhiliaoapp.musically",     True],
                       ["YouTube",    "com.google.android.youtube",   True],
                       ["WhatsApp",   "com.whatsapp",                 False],
                       ["Twitter",    "com.twitter.android",          False],
                       ["Facebook",   "com.facebook.katana",          False],
                       ["Netflix",    "com.netflix.mediaclient",       False]]
#Matriz de apps bloqueadas en la sesion actual
MatrizAppsBloqueadasSesionActual=[] #Matriz vacia que va a ir creciendo

#busca si el usuario creado ya existe
def buscar_usuario(nombre):
    for i in range(len(matrizdataUsuarios)):
        nombreUsuario= matrizdataUsuarios[i][0]
        if nombreUsuario==nombre:
            return i
        
    return -1


def registro_sesion(nombre, minutos, puntos, exito):
    global MatrizHistorialSesiones

    #Agregar un arreglo de nueva sesion al historialSesiones 
    nueva_sesion=[nombre, minutos, puntos, exito ]
    #.append : agrega la nueva fila al final
    MatrizHistorialSesiones.append(nueva_sesion)

    indice=buscar_usuario(nombre) #Buscar si el usuario existe

    if indice==-1: #La funcion buscar_Usuario devuelve un -1, lo que significa que busco en matrizDataUsuarios y no encontro el nombre 
        nuevoUsuario=[nombre, 0,0,0,0 ]
        matrizdataUsuarios.append(nuevoUsuario)
        indice =len(matrizdataUsuarios)-1

    ##Actualizar la fila del usuario en la matrizDataUsuarios (puntos)
    matrizdataUsuarios[indice][1]= matrizdataUsuarios[indice][1] + puntos
    

    if exito==True:
        #(racha)
        matrizdataUsuarios[indice][2]=matrizdataUsuarios[indice][2]+ 1
        #(Sesiones ok)
        matrizdataUsuarios[indice][3]=matrizdataUsuarios[indice][3]+ 1
    else:
        #(Reinciar racha)
        matrizdataUsuarios[indice][2]=0
        #(Sesiones Fallidas)
        matrizdataUsuarios[indice][4]=matrizdataUsuarios[indice][4]+ 1

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
    tasa=0.0
    if totalSesiones>0:
        tasa=(SesionesOkU/totalSesiones)*100 
    
    #Calcular promedio de puntos por sesion exitosa
  ##  promedio=calcular_promedio_usuario(nombre)

    #Mostrar al usuario
    print("\n" + "=" * 42)
    print(f"Usuario: {NombreU}")
    print("\n" + "=" * 42)
    print(f"Puntos totales: {PuntosU}")
    print(f"Racha actual: {RachaU} dias ")
    print(f"Sesiones exitosas: {SesionesOkU}")
    print(f"Sesiones fallidas: {SesionesFallidasU}")
    print(f"Tasa de exito: {tasa}%")
 ##   print(f"Promedio de puntos por sesion: {promedio} pts")

    #Mostrar ultimas 5 sesiones????????

def calcular_promedio_usuario(nombre):
    totalpuntos=0
    ContadorSesiones=0
    for i in range(len(MatrizHistorialSesiones)):
        sesion=MatrizHistorialSesiones[i]
        nombre_s=sesion[0]
        puntos_s=sesion[2]
        Exito_s=sesion[3]

        if nombre_s==nombre and Exito_s==True and puntos_s>0:
            totalpuntos=totalpuntos+puntos_s
            ContadorSesiones=ContadorSesiones+1
    promedio=totalpuntos/ContadorSesiones
    return promedio




###### menuuuuu#########


# Arreglo con las opciones del menu principal
OPCIONES_MENU: list = [
    "1. Iniciar sesion de enfoque",
    "2. Ver ranking semanal",
    "3. Ver mi perfil",
    "4. Cambiar usuario",
    "5. Salir"
]

# Arreglo con los modos de sesion disponibles
MODOS_SESION: list = ["Normal", "Examen", "Pomodoro"]

# Matriz con duraciones y sus puntos base
# Cada fila es: [duracion_minutos, puntos_base, descripcion]
DURACIONES: list = [
    [25,  20,  "Pomodoro basico"],
    [50,  45,  "Sesion media   "],
    [90,  80,  "Sesion estandar"],
    [120, 120, "Sesion extendida"]
]



#Pide el nombre del usuario al iniciar el programa.
def pedir_nombre_usuario():
    
    print("\n" + "=" * 42)
    print("   Bienvenido a GRINDLOCK")
    print("=" * 42)
    nombre = input("   Ingresa tu nombre: ")

    # Validacion basica: si esta vacio, poner nombre por defecto
    if nombre.strip() == "":                        # OPERADORES: comparacion
        nombre = "Estudiante"

    return nombre.strip()                           # RETURN

#Imprime el menu principal con el nombre del usuario
def mostrar_menu():
    
    print("\n" + "=" * 42)
    print("   GRINDLOCK - Sin distracciones.")
    print("=" * 42)
    print(f"   Usuario: {nombre_usuario}")
    print(f"   Sesiones completadas: {sesiones_ok}")
    print("=" * 42)

    # FOR: recorre el arreglo de opciones para mostrarlas
    for opcion in OPCIONES_MENU:
        print(f"   {opcion}")

    print("=" * 42)

#Muestra las opciones de duracion con sus puntos.
def mostrar_menu_duracion():
    
    print("\n   Elige la duracion de tu sesion:")
    print("   " + "-" * 34)

    # FOR con indice sobre la MATRIZ de duraciones
    for i in range(len(DURACIONES)):
        fila = DURACIONES[i]                        # Acceso a fila de la matriz
        duracion: int = fila[0]                     # Columna 0: minutos
        puntos: int   = fila[1]                     # Columna 1: puntos
        desc: str     = fila[2]                     # Columna 2: descripcion
        print(f"   {i + 1}. {desc}  -  {duracion} min  (+{puntos} pts)")

    print("   " + "-" * 34)




#Funcion principal: el WHILE que mantiene el programa vivo.
def menu_principal():
    
    global nombre_usuario

    # Pedir nombre antes de entrar al menu
    nombre_usuario = pedir_nombre_usuario()
    print(f"\n   Bienvenido, {nombre_usuario}!")

    activo= True                             # Variable de control del WHILE

    # WHILE principal - se repite hasta que el usuario elija salir
    while activo:
        mostrar_menu()
        opcion=int(input("Elige tu opcion: "))
        # SWITCH / MATCH / CASE - una rama por opcion
        match opcion:
            case 1:
               print("=====SESIONES=====")
               guardian=input("Escribe el nombre de tu guardian: ")
               menu=int(input("Cuantos minutos quiere estar concentrado\n  1. 25 min (+20 pts)\n  2. 50 min (+45 pts)\n  3. 90 min (+80 pts)\n  4. 120 min (+120 pts)\n  5.Personalizar\n"))

#menu con todas las opciones del temporizador dependiendo de lo que escoge el usuario, se rescriben las variables para la funcion temporizador
               match menu:
                    case 1:
                        min=25
                        sec=0
                        timer=min*60+sec
                        min=timer//60
                        sec=timer-(min*60)
                        contraseña=iniciar_sesion_clave(timer, guardian)
                        print(contraseña)
                        temporizador(timer,min,sec,contraseña)
                        if acabo==True:
                            points=puntos(timer)
                            print(points)
                    case 2:
                        min=50
                        sec=0
                        timer=min*60+sec
                        min=timer//60
                        sec=timer-(min*60)
                        contraseña=iniciar_sesion_clave(timer, guardian)
                        temporizador(timer,min,sec,contraseña)
                        if acabo==True:
                            points=puntos(timer)
                            print(points)
                    case 3:
                        min=90
                        sec=0
                        timer=min*60+sec
                        min=timer//60
                        sec=timer-(min*60)
                        contraseña=iniciar_sesion_clave(timer, guardian)
                        temporizador(timer,min,sec,contraseña)
                        if acabo==True:
                            points=puntos(timer)
                            print(points)
                    case 4:
                        min=120
                        sec=0
                        timer=min*60+sec
                        min=timer//60
                        sec=timer-(min*60)
                        contraseña=iniciar_sesion_clave(timer, guardian)
                        temporizador(timer,min,sec,contraseña)
                        if acabo==True:
                            points=puntos(timer)
                            print(points)
                    case 5:
                        min=int(input("Cuantos minutos quiere estar concentrado?: "))
                        sec=int(input("Cuantos segundos?: "))
                        timer=min*60+sec
                        contraseña=iniciar_sesion_clave(timer, guardian)
                        print(contraseña)
                        acabo=temporizador(timer,min,sec,contraseña)
                        if acabo==True:
                            points=puntos(timer)
                            print(points)

            case 2:
               print()
            case 3:
                lol=int(input("Quieres ver un resumen o ver tu nivel?: \n  1.Resumen\n  2.Nivel\n"))
                match lol:
                    case 1:
                        resumen_puntos()
                    case 2:
                        nivel(puntos_totales)
                    case _:
                        print("Opcion invalida, vuelve a intentar")
            case 4:
                print()
            case 5:
                activo = False                      # Sale del WHILE
                print("\n   Hasta la proxima sesion. Sigue enfocado!")
            case _:
                print("   Opcion invalida. Intenta de nuevo.")


# Punto de entrada del programa
if __name__ == "__main__":
    menu_principal()
    
