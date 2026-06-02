import json

# cada entidad tiene su propio archivo json
ARCHIVO_PELICULAS = "data/peliculas.json"
ARCHIVO_FUNCIONES = "data/funciones.json"
ARCHIVO_RESERVAS  = "data/reservas.json"

# ── películas ──────────────────────────────────
def cargar_peliculas():
    try:
        with open(ARCHIVO_PELICULAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        guardar_peliculas([])
        return []

def guardar_peliculas(peliculas):
    with open(ARCHIVO_PELICULAS, "w", encoding="utf-8") as f:
        json.dump(peliculas, f, indent=4, ensure_ascii=False)

# ── funciones ──────────────────────────────────
def cargar_funciones():
    try:
        with open(ARCHIVO_FUNCIONES, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        guardar_funciones([])
        return []

def guardar_funciones(funciones):
    with open(ARCHIVO_FUNCIONES, "w", encoding="utf-8") as f:
        json.dump(funciones, f, indent=4, ensure_ascii=False)

# ── reservas ──────────────────────────────────
def cargar_reservas():
    try:
        with open(ARCHIVO_RESERVAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        guardar_reservas([])
        return []

def guardar_reservas(reservas):
    with open(ARCHIVO_RESERVAS, "w", encoding="utf-8") as f:
        json.dump(reservas, f, indent=4, ensure_ascii=False)    