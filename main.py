"""
  ____          _____               _ _           _       
 |  _ \        |  __ \             (_) |         | |      
 | |_) |_   _  | |__) |_ _ _ __ _____| |__  _   _| |_ ___ 
 |  _ <| | | | |  ___/ _` | '__|_  / | '_ \| | | | __/ _ \
 | |_) | |_| | | |  | (_| | |   / /| | |_) | |_| | ||  __/
 |____/ \__, | |_|   \__,_|_|  /___|_|_.__/ \__, |\__\___|
         __/ |                               __/ |        
        |___/                               |___/         
    
____________________________________
/ Si necesitas ayuda, contáctame en \
\ https://parzibyte.me               /
 ------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
Creado por Parzibyte (https://parzibyte.me).
------------------------------------------------------------------------------------------------
            | IMPORTANTE |
Si vas a borrar este encabezado, considera:
Seguirme: https://parzibyte.me/blog/sigueme/
Y compartir mi blog con tus amigos
También tengo canal de YouTube: https://www.youtube.com/channel/UCroP4BTWjfM0CkGB6AFUoBg?sub_confirmation=1
Twitter: https://twitter.com/parzibyte
Facebook: https://facebook.com/parzibyte.fanpage
Instagram: https://instagram.com/parzibyte
Hacer una donación vía PayPal: https://paypal.me/LuisCabreraBenito
------------------------------------------------------------------------------------------------
"""
import random
from copy import deepcopy
from colorama import init, Fore, Style

init()

MINIMO_FILAS = 5
MAXIMO_FILAS = 10
MINIMO_COLUMNAS = 6
MAXIMO_COLUMNAS = 10
ESPACIO_VACIO = " "
COLOR_1 = "x"
COLOR_2 = "o"
JUGADOR_1 = 1
# La CPU también es el jugador 2
JUGADOR_2 = 2
CONECTA = 4
ESTA_JUGANDO_CPU = False


def solicitar_entero_valido(mensaje):
    """
    Solicita un número entero y lo sigue solicitando
    mientras no sea un entero válido
    """
    while True:
        try:
            posible_entero = int(input(mensaje))
            return posible_entero
        except ValueError:
            continue


def solicitar_columnas():
    while True:
        columnas = solicitar_entero_valido("Ingresa el número de columnas:")
        if columnas < MINIMO_COLUMNAS or columnas > MAXIMO_COLUMNAS:
            print(f"El mínimo de columnas es {MINIMO_COLUMNAS} y el máximo {MAXIMO_COLUMNAS}")
        else:
            return columnas


def solicitar_filas():
    while True:
        filas = solicitar_entero_valido("Ingresa el número de filas:")
        if filas < MINIMO_FILAS or filas > MAXIMO_FILAS:
            print(f"El mínimo de filas es {MINIMO_FILAS} y el máximo {MAXIMO_FILAS}")
        else:
            return filas


def crear_tablero(filas, columnas):
    tablero = []
    for fila in range(filas):
        tablero.append([])
        for columna in range(columnas):
            tablero[fila].append(ESPACIO_VACIO)
    return tablero


def imprimir_tablero(tablero):
    # Imprime números de columnas
    print("|", end="")
    for f in range(1, len(tablero[0]) + 1):
        print(f, end="|")
    print("")
    # Datos
    for fila in tablero:
        print("|", end="")
        for valor in fila:
            color_terminal = Fore.GREEN
            if valor == COLOR_2:
                color_terminal = Fore.RED
            print(color_terminal + valor, end="")
            print(Style.RESET_ALL, end="")
            print("|", end="")
        print("")
    # Pie
    print("+", end="")
    for f in range(1, len(tablero[0]) + 1):
        print("-", end="+")
    print("")


def obtener_fila_valida_en_columna(columna, tablero):
    indice = len(tablero) - 1
    while indice >= 0:
        if tablero[indice][columna] == ESPACIO_VACIO:
            return indice
        indice -= 1
    return -1


def solicitar_columna(tablero):
    """
    Solicita la columna y devuelve la columna ingresada -1 para ser usada fácilmente como índice
    """
    while True:
        columna = solicitar_entero_valido("Ingresa la columna para colocar la pieza: ")
        if columna <= 0 or columna > len(tablero[0]):
            print("Columna no válida")
        elif tablero[0][columna - 1] != ESPACIO_VACIO:
            print("Esa columna ya está llena")
        else:
            return columna - 1


def colocar_pieza(columna, jugador, tablero):
    """
    Coloca una pieza en el tablero. La columna debe
    comenzar en 0
    """
    color = COLOR_1
    if jugador == JUGADOR_2:
        color = COLOR_2
    fila = obtener_fila_valida_en_columna(columna, tablero)
    if fila == -1:
        return False
    tablero[fila][columna] = color
    return True


def obtener_conteo_derecha(fila, columna, color, tablero):
    fin_columnas = len(tablero[0])
    contador = 0
    for i in range(columna, fin_columnas):
        if contador >= CONECTA:
            return contador
        if tablero[fila][i] == color:
            contador += 1
        else:
            contador = 0
    return contador


def obtener_conteo_izquierda(fila, columna, color, tablero):
    contador = 0
    # -1 porque no es inclusivo
    for i in range(columna, -1, -1):
        if contador >= CONECTA:
            return contador
        if tablero[fila][i] == color:
            contador += 1
        else:
            contador = 0

    return contador


def obtener_conteo_abajo(fila, columna, color, tablero):
    fin_filas = len(tablero)
    contador = 0
    for i in range(fila, fin_filas):
        if contador >= CONECTA:
            return contador
        if tablero[i][columna] == color:
            contador += 1
        else:
            contador = 0
    return contador


def obtener_conteo_arriba(fila, columna, color, tablero):
    contador = 0
    for i in range(fila, -1, -1):
        if contador >= CONECTA:
            return contador
        if contador >= CONECTA:
            return contador
        if tablero[i][columna] == color:
            contador += 1
        else:
            contador = 0
    return contador


def obtener_conteo_arriba_derecha(fila, columna, color, tablero):
    contador = 0
    numero_fila = fila
    numero_columna = columna
    while numero_fila >= 0 and numero_columna < len(tablero[0]):
        if contador >= CONECTA:
            return contador
        if tablero[numero_fila][numero_columna] == color:
            contador += 1
        else:
            contador = 0
        numero_fila -= 1
        numero_columna += 1
    return contador


def obtener_conteo_arriba_izquierda(fila, columna, color, tablero):
    contador = 0
    numero_fila = fila
    numero_columna = columna
    while numero_fila >= 0 and numero_columna >= 0:
        if contador >= CONECTA:
            return contador
        if tablero[numero_fila][numero_columna] == color:
            contador += 1
        else:
            contador = 0
        numero_fila -= 1
        numero_columna -= 1
    return contador


def obtener_conteo_abajo_izquierda(fila, columna, color, tablero):
    contador = 0
    numero_fila = fila
    numero_columna = columna
    while numero_fila < len(tablero) and numero_columna >= 0:
        if contador >= CONECTA:
            return contador
        if tablero[numero_fila][numero_columna] == color:
            contador += 1
        else:
            contador = 0
        numero_fila += 1
        numero_columna -= 1
    return contador


def obtener_conteo_abajo_derecha(fila, columna, color, tablero):
    contador = 0
    numero_fila = fila
    numero_columna = columna
    while numero_fila < len(tablero) and numero_columna < len(tablero[0]):
        if contador >= CONECTA:
            return contador
        if tablero[numero_fila][numero_columna] == color:
            contador += 1
        else:
            contador = 0
        numero_fila += 1
        numero_columna += 1
    return contador


def obtener_direcciones():
    return [
        'izquierda',
        'arriba',
        'abajo',
        'derecha',
        'arriba_derecha',
        'abajo_derecha',
        'arriba_izquierda',
        'abajo_izquierda',
    ]


def obtener_conteo(fila, columna, color, tablero):
    direcciones = obtener_direcciones()
    for direccion in direcciones:
        funcion = globals()['obtener_conteo_' + direccion]
        conteo = funcion(fila, columna, color, tablero)
        if conteo >= CONECTA:
            return conteo
    return 0


def obtener_color_de_jugador(jugador):
    color = COLOR_1
    if jugador == JUGADOR_2:
        color = COLOR_2
    return color


def comprobar_ganador(jugador, tablero):
    color = obtener_color_de_jugador(jugador)
    for f, fila in enumerate(tablero):
        for c, celda in enumerate(fila):
            conteo = obtener_conteo(f, c, color, tablero)
            if conteo >= CONECTA:
                return True
    return False


def elegir_jugador_al_azar():
    return random.choice([JUGADOR_1, JUGADOR_2])


def imprimir_y_solicitar_turno(turno, tablero):
    if not ESTA_JUGANDO_CPU:
        print(f"Jugador 1: {COLOR_1} | Jugador 2: {COLOR_2}")
    else:
        print(f"Jugador 1: {COLOR_1} | CPU: {COLOR_2}")
    if turno == JUGADOR_1:
        print(f"Turno del jugador 1 ({COLOR_1})")
    else:
        if not ESTA_JUGANDO_CPU:
            print(f"Turno del jugador 2 ({COLOR_2})")
        else:
            print("Turno de la CPU")
    return solicitar_columna(tablero)


def felicitar_jugador(jugador_actual):
    if not ESTA_JUGANDO_CPU:
        if jugador_actual == JUGADOR_1:
            print("Felicidades Jugador 1. Has ganado")
        else:
            print("Felicidades Jugador 2. Has ganado")
    else:
        if jugador_actual == JUGADOR_1:
            print("Felicidades Jugador 1. Has ganado")
        else:
            print("Ha ganado el CPU")


def es_empate(tablero):
    for columna in range(len(tablero[0])):
        if obtener_fila_valida_en_columna(columna, tablero) != -1:
            return False
    return True


def indicar_empate():
    print("Empate")


def obtener_tiradas_faltantes_en_columna(columna, tablero):
    indice = len(tablero) - 1
    tiradas = 0
    while indice >= 0:
        if tablero[indice][columna] == ESPACIO_VACIO:
            tiradas += 1
        indice -= 1
    return tiradas


def obtener_tiradas_faltantes(tablero):
    tiradas = 0
    for columna in range(len(tablero[0])):
        tiradas += obtener_tiradas_faltantes_en_columna(columna, tablero)
    return tiradas


def imprimir_tiradas_faltantes(tablero):
    print("Tiradas faltantes: " + str(obtener_tiradas_faltantes(tablero)))


def jugador_vs_jugador(tablero):
    jugador_actual = elegir_jugador_al_azar()
    while True:
        imprimir_tablero(tablero)
        imprimir_tiradas_faltantes(tablero)
        columna = imprimir_y_solicitar_turno(jugador_actual, tablero)
        pieza_colocada = colocar_pieza(columna, jugador_actual, tablero)
        if not pieza_colocada:
            print("No se puede colocar en esa columna")
        ha_ganado = comprobar_ganador(jugador_actual, tablero)
        if ha_ganado:
            imprimir_tablero(tablero)
            felicitar_jugador(jugador_actual)
            break
        elif es_empate(tablero):
            imprimir_tablero(tablero)
            indicar_empate()
            break
        else:
            if jugador_actual == JUGADOR_1:
                jugador_actual = JUGADOR_2
            else:
                jugador_actual = JUGADOR_1


def obtener_columna_segun_cpu(jugador, tablero):
    return elegir_columna_ideal(jugador, tablero)


def obtener_jugador_contrario(jugador):
    if jugador == JUGADOR_1:
        return JUGADOR_2
    return JUGADOR_1


def elegir_columna_ideal(jugador, tableroOriginal):
    """
    Reglas:
    1- Si hay un movimiento para ganar, tomarlo
    2- Si el oponente tiene un movimiento para ganar, evitarlo
    3- Si nada de lo de arriba se cumple, buscar columna en donde se obtendría el mayor puntaje
    4- Si lo de arriba no se cumple, buscar columna en donde el adversario obtendría el mayor puntaje
    5- Preferir tomar cosas centrales antes de bordes
    """
    tablero = deepcopy(tableroOriginal)
    # Puedo ganar?
    columna_ganadora = obtener_columna_ganadora(jugador, tablero)
    if columna_ganadora != -1:
        return columna_ganadora
    # Si no, mi oponente puede ganar? en caso de que sí, debo evitarlo
    columna_perdedora = obtener_columna_ganadora(obtener_jugador_contrario(jugador), tablero)
    if columna_perdedora != -1:
        return columna_perdedora

    umbral_puntaje = 1
    # Si no, buscaré un lugar en donde al colocar mi pieza me dé más posibilidades de conectar 4
    puntaje_ganador, columna_mia = obtener_columna_con_mayor_puntaje(jugador, tablero)
    # Pero también necesito el de mi adversario
    puntaje_ganador_adversario, columna_adversario = obtener_columna_con_mayor_puntaje(
        obtener_jugador_contrario(jugador), tablero)
    if puntaje_ganador > umbral_puntaje and puntaje_ganador_adversario > umbral_puntaje:
        # Aquí se puede elegir entre ataque o defensa. Se prefiere la defensa
        if puntaje_ganador_adversario > puntaje_ganador:
            return columna_adversario
        else:
            return columna_mia
    # Si lo demás falla, elegir una columna central
    central = obtener_columna_central(jugador, tablero)
    if central != -1:
        return central
    # Y de últimas, elegir la primer columna que no esté vacía
    columna_disponible = obtener_primera_columna_vacia(jugador, tablero)
    if columna_disponible != -1:
        return columna_disponible
    # Si no, no sé qué más hacer. Esto no debería pasar
    print("Error. No se debería llegar hasta aquí")


def obtener_primera_columna_vacia(jugador, tableroOriginal):
    tablero = deepcopy(tableroOriginal)
    for indice in range(len(tablero[0])):
        if colocar_pieza(indice, jugador, tablero):
            return indice


def obtener_columna_central(jugador, tableroOriginal):
    tablero = deepcopy(tableroOriginal)
    mitad = int((len(tablero[0]) - 1) / 2)
    if colocar_pieza(mitad, jugador, tablero):
        return mitad
    return -1


def obtener_primera_fila_no_vacia(columna, tablero):
    for indice_fila, fila in enumerate(tablero):
        if fila[columna] != ESPACIO_VACIO:
            return indice_fila
    return -1


def obtener_columna_con_mayor_puntaje(jugador, tableroOriginal):
    conteo_mayor = 0
    indice_columna_mayor = -1
    for indiceColumna in range(len(tableroOriginal)):
        tablero = deepcopy(tableroOriginal)
        pieza_colocada = colocar_pieza(indiceColumna, jugador, tablero)
        if pieza_colocada:
            fila = obtener_primera_fila_no_vacia(indiceColumna, tablero)
            if fila != -1:
                conteo = obtener_conteo(fila, indiceColumna, obtener_color_de_jugador(jugador), tablero)
                if conteo > conteo_mayor:
                    conteo_mayor = conteo
                    indice_columna_mayor = indiceColumna
    return conteo_mayor, indice_columna_mayor


def obtener_columna_ganadora(jugador, tableroOriginal):
    for indiceColumna in range(len(tableroOriginal)):
        tablero = deepcopy(tableroOriginal)
        pieza_colocada = colocar_pieza(indiceColumna, jugador, tablero)
        if pieza_colocada:
            gana = comprobar_ganador(jugador, tablero)
            if gana:
                return indiceColumna
    return -1


def jugador_vs_computadora(tablero):
    global ESTA_JUGANDO_CPU
    ESTA_JUGANDO_CPU = True
    jugador_actual = elegir_jugador_al_azar()
    while True:
        imprimir_tablero(tablero)
        imprimir_tiradas_faltantes(tablero)
        if jugador_actual == JUGADOR_1:
            columna = imprimir_y_solicitar_turno(jugador_actual, tablero)
        else:
            print("CPU pensando...")
            columna = obtener_columna_segun_cpu(jugador_actual, tablero)
        pieza_colocada = colocar_pieza(columna, jugador_actual, tablero)
        if not pieza_colocada:
            print("No se puede colocar en esa columna")
        ha_ganado = comprobar_ganador(jugador_actual, tablero)
        if ha_ganado:
            imprimir_tablero(tablero)
            felicitar_jugador(jugador_actual)
            break
        elif es_empate(tablero):
            imprimir_tablero(tablero)
            indicar_empate()
            break
        else:
            if jugador_actual == JUGADOR_1:
                jugador_actual = JUGADOR_2
            else:
                jugador_actual = JUGADOR_1
    ESTA_JUGANDO_CPU = False


def volver_a_jugar():
    while True:
        eleccion = input("¿Quieres volver a jugar? [s/n] ").lower()
        if eleccion == "s":
            return True
        elif eleccion == "n":
            return False


def main():
    while True:
        eleccion = input("1- Jugador vs Jugador"
                         "\n"
                         "2- Jugador vs Máquina"
                         "\n"
                         "4- Salir"
                         "\n"
                         "Elige: ")
        if eleccion == "4":
            break

        if eleccion == "1":
            filas, columnas = solicitar_filas(), solicitar_columnas()
            while True:
                tablero = crear_tablero(filas, columnas)
                jugador_vs_jugador(tablero)
                if not volver_a_jugar():
                    break
        if eleccion == "2":
            filas, columnas = solicitar_filas(), solicitar_columnas()
            while True:
                tablero = crear_tablero(filas, columnas)
                jugador_vs_computadora(tablero)
                if not volver_a_jugar():
                    break


main()
