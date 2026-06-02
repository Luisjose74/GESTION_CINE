"""datos.py Gestión centralizada de archivos JSON.
Todas las lecturas y escrituras de datos pasan por este módulo.
"""

import json
import os

# Rutas de los archivos JSON
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #obtener la ruta de la carpeta base
DATA_DIR = os.path.join(BASE_DIR, "data") #obtener la ruta de la carpeta de datos

RUTA_PELICULAS  = os.path.join(DATA_DIR, "peliculas.json") #definir la ruta del archivo JSON para las películas
RUTA_FUNCIONES  = os.path.join(DATA_DIR, "funciones.json")
RUTA_RESERVAS   = os.path.join(DATA_DIR, "reservas.json")
RUTA_COMBOS     = os.path.join(DATA_DIR, "combos.json")
RUTA_PEDIDOS_COMIDA = os.path.join(DATA_DIR, "pedidos_comida.json")


#definir función para cargar una lista desde un archivo JSON, manejando los casos en los que el archivo no exista o esté vacío
def _cargar(ruta: str) -> list:
    
    try: #intentar abrir el archivo JSON y cargar su contenido como una lista, 
        #si el archivo no existe o está vacío, devolver una lista vacía
        with open(ruta, "r", encoding="utf-8") as f: #abrir el archivo en modo lectura
            return json.load(f) #leer el contenido del archivo y devolverlo como una lista
    except FileNotFoundError: #si el archivo no existe, devolver una lista vacía
        return []
    except json.JSONDecodeError: #si el archivo está vacío o no contiene una lista válida, devolver una lista vacía
        return []

#definir función para guardar una lista en un archivo JSON, creando la carpeta si no existe y manejando posibles errores de escritura
def _guardar(ruta: str, datos: list) -> None: 
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True) #crear la carpeta de datos si no existe (exist_ok=True evita errores si la carpeta ya existe)
        with open(ruta, "w", encoding="utf-8") as f: #abrir el archivo en modo escritura (esto creará el archivo si no existe o lo sobrescribirá si ya existe)
            json.dump(datos, f, indent=4, ensure_ascii=False) #escribir el contenido de la lista en el archivo
    except OSError as e: #si ocurre un error de escritura
        print(f"[ERROR] No se pudo guardar el archivo {ruta}: {e}") #imprimir un mensaje de error


# Películas 
#definir función para cargar la lista de películas desde el archivo JSON utilizando la función _cargar
def cargar_peliculas() -> list: 
    return _cargar(RUTA_PELICULAS) #devolver la lista de películas cargada desde el archivo JSON

#definir función para guardar la lista de películas en el archivo JSON utilizando la función _guardar
def guardar_peliculas(peliculas: list) -> None: #
    _guardar(RUTA_PELICULAS, peliculas) #guardar la lista de películas en el archivo JSON


# Funciones 
def cargar_funciones() -> list:
    return _cargar(RUTA_FUNCIONES)

def guardar_funciones(funciones: list) -> None:
    _guardar(RUTA_FUNCIONES, funciones)


# Reservas
def cargar_reservas() -> list:
    return _cargar(RUTA_RESERVAS)

def guardar_reservas(reservas: list) -> None:
    _guardar(RUTA_RESERVAS, reservas)


# Combos de comida 
def cargar_combos() -> list:
    return _cargar(RUTA_COMBOS)

def guardar_combos(combos: list) -> None:
    _guardar(RUTA_COMBOS, combos)


# Pedidos de comida 
def cargar_pedidos_comida() -> list:
    return _cargar(RUTA_PEDIDOS_COMIDA)

def guardar_pedidos_comida(pedidos: list) -> None:
    _guardar(RUTA_PEDIDOS_COMIDA, pedidos)
