 #============================================================
# peliculas.py
# ============================================================
# Este archivo sirve para administrar películas de un cine.
#
# CRUD significa:
# C -> Crear
# R -> Leer
# U -> Actualizar
# D -> Eliminar
# ============================================================


# ------------------------------------------------------------
# IMPORTACIONES
# ------------------------------------------------------------

# Importa la consola bonita de Rich
from rich.console import Console

# Importa tablas bonitas
from rich.table import Table

# Prompt -> pedir texto
# IntPrompt -> pedir números enteros
from rich.prompt import Prompt, IntPrompt

# Importa cuadros decorativos
from rich.panel import Panel

# Importa funciones para cargar y guardar películas
from modules.datos import cargar_peliculas, guardar_peliculas


# ------------------------------------------------------------
# CREAR CONSOLA
# ------------------------------------------------------------

# Creamos la consola principal
console = Console()


# ------------------------------------------------------------
# FUNCIÓN PARA GENERAR IDs
# ------------------------------------------------------------

# Función que crea IDs automáticos
# peliculas: recibe la lista de películas
# -> int: devuelve un número entero
def _generar_id(peliculas: list) -> int:

    # Verifica si la lista está vacía
    if not peliculas:

        # Si no hay películas devuelve ID 1
        return 1

    # Busca el ID más alto y suma 1
    return max(p["id_pelicula"] for p in peliculas) + 1


# ------------------------------------------------------------
# FUNCIÓN PARA BUSCAR PELÍCULA POR ID
# ------------------------------------------------------------

# Busca una película usando su ID
def _buscar_por_id(peliculas: list, id_pelicula: int):

    # Recorremos cada película
    for p in peliculas:

        # Comparamos el ID de la película
        if p["id_pelicula"] == id_pelicula:

            # Si coincide devuelve la película
            return p

    # Si no encontró nada devuelve None
    return None


# ------------------------------------------------------------
# MOSTRAR TABLA DE PELÍCULAS
# ------------------------------------------------------------

# Función que muestra películas en una tabla
def mostrar_tabla_peliculas(peliculas: list) -> None:

    # Verifica si no existen películas
    if not peliculas:

        # Mensaje de advertencia
        console.print("[yellow]⚠️ No hay películas registradas.[/yellow]")

        # Sale de la función
        return

    # Creamos una tabla
    tabla = Table(

        # Título de la tabla
        title="🎬 Catálogo de Películas",

        # Color del borde
        border_style="cyan",

        # Color del encabezado
        header_style="bold magenta"
    )

    # Creamos columna ID
    tabla.add_column(

        # Nombre de la columna
        "ID",

        # Estilo del texto
        style="bold cyan",

        # Centrar contenido
        justify="center"
    )

    # Columna título
    tabla.add_column(

        # Nombre de columna
        "Título",

        # Color y estilo
        style="bold white"
    )

    # Columna género
    tabla.add_column(

        # Nombre de columna
        "Género",

        # Color amarillo
        style="yellow"
    )

    # Columna duración
    tabla.add_column(

        # Nombre de columna
        "Duración",

        # Color verde
        style="green",

        # Centrar texto
        justify="center"
    )

    # Recorremos todas las películas
    for p in peliculas:

        # Agregamos una fila
        tabla.add_row(

            # Convertimos ID a texto
            str(p["id_pelicula"]),

            # Título
            p["titulo"],

            # Género
            p["genero"],

            # Duración con texto min
            f"{p['duracion_min']} min"
        )

    # Mostramos la tabla
    console.print(tabla)


# ------------------------------------------------------------
# CREAR PELÍCULA
# ------------------------------------------------------------

# Función para agregar películas
def crear_pelicula() -> None:

    # Muestra panel decorativo
    console.print(

        # Panel bonito
        Panel(

            # Texto del panel
            "[bold cyan]➕ Nueva Película[/bold cyan]",

            # Evita ocupar toda la pantalla
            expand=False
        )
    )

    # Carga películas guardadas
    peliculas = cargar_peliculas()

    # Pide el título al usuario
    titulo = Prompt.ask(

        # Texto que verá el usuario
        "  Título de la película"

    # Elimina espacios innecesarios
    ).strip()

    # Verifica si quedó vacío
    if not titulo:

        # Muestra error
        console.print(

            # Texto rojo
            "[red]✗ El título no puede estar vacío.[/red]"
        )

        # Sale de la función
        return

    # Pide género
    genero = Prompt.ask(

        # Texto guía
        "  Género (Acción / Comedia / Terror / Drama / Animación / otro)"

    # Quita espacios
    ).strip()

    # Inicia manejo de errores
    try:

        # Pide duración
        duracion = IntPrompt.ask(

            # Mensaje
            "  Duración en minutos"
        )

        # Verifica si es menor o igual a 0
        if duracion <= 0:

            # Genera error manualmente
            raise ValueError

    # Captura errores
    except (ValueError, Exception):

        # Mensaje de error
        console.print(

            # Texto rojo
            "[red]✗ La duración debe ser un número entero positivo.[/red]"
        )

        # Sale
        return

    # Creamos el diccionario de la película
    nueva = {

        # ID automático
        "id_pelicula": _generar_id(peliculas),

        # Guardar título
        "titulo": titulo,

        # Guardar género
        "genero": genero,

        # Guardar duración
        "duracion_min": duracion
    }

    # Agrega película a la lista
    peliculas.append(nueva)

    # Guarda cambios
    guardar_peliculas(peliculas)

    # Mensaje de éxito
    console.print(

        # Texto verde
        f"[green]✔️ Película '[bold]{titulo}[/bold]' agregada con ID {nueva['id_pelicula']}.[/green]"
    )


# ------------------------------------------------------------
# LEER PELÍCULAS
# ------------------------------------------------------------

# Función para mostrar películas
def leer_peliculas() -> None:

    # Carga películas guardadas
    peliculas = cargar_peliculas()

    # Muestra la tabla
    mostrar_tabla_peliculas(peliculas)


# ------------------------------------------------------------
# ACTUALIZAR PELÍCULA
# ------------------------------------------------------------

# Función para modificar películas
def actualizar_pelicula() -> None:

    # Muestra panel decorativo
    console.print(

        # Panel
        Panel(

            # Texto del panel
            "[bold yellow]✏️ Actualizar Película[/bold yellow]",

            # Tamaño ajustado
            expand=False
        )
    )

    # Carga películas
    peliculas = cargar_peliculas()

    # Muestra películas
    mostrar_tabla_peliculas(peliculas)

    # Verifica si no hay películas
    if not peliculas:

        # Sale
        return

    # Intenta pedir ID
    try:

        # Pide número
        id_buscar = IntPrompt.ask(

            # Mensaje
            "  ID de la película a actualizar"
        )

    # Captura error
    except Exception:

        # Mensaje rojo
        console.print("[red]✗ ID inválido.[/red]")

        # Sale
        return

    # Busca película
    pelicula = _buscar_por_id(

        # Lista de películas
        peliculas,

        # ID buscado
        id_buscar
    )

    # Verifica si existe
    if not pelicula:

        # Error
        console.print(

            # Texto rojo
            f"[red]✗ No existe una película con ID {id_buscar}.[/red]"
        )

        # Sale
        return

    # Muestra qué película se editará
    console.print(

        # Texto
        f"  Editando: [bold]{pelicula['titulo']}[/bold]"
    )

    # Pide nuevo título
    nuevo_titulo = Prompt.ask(

        # Mensaje
        "  Nuevo título",

        # Valor por defecto
        default=pelicula["titulo"]

    # Limpia espacios
    ).strip()

    # Pide nuevo género
    nuevo_genero = Prompt.ask(

        # Mensaje
        "  Nuevo género",

        # Valor por defecto
        default=pelicula["genero"]

    # Limpia espacios
    ).strip()

    # Manejo de errores
    try:

        # Pide nueva duración
        nueva_duracion = IntPrompt.ask(

            # Texto
            "  Nueva duración (min)",

            # Valor actual
            default=pelicula["duracion_min"]
        )

        # Valida duración
        if nueva_duracion <= 0:

            # Genera error
            raise ValueError

    # Captura errores
    except Exception:

        # Mensaje de error
        console.print(

            # Texto rojo
            "[red]✗ Duración inválida, se conserva el valor anterior.[/red]"
        )

        # Mantiene duración anterior
        nueva_duracion = pelicula["duracion_min"]

    # Actualiza título
    pelicula["titulo"] = nuevo_titulo

    # Actualiza género
    pelicula["genero"] = nuevo_genero

    # Actualiza duración
    pelicula["duracion_min"] = nueva_duracion

    # Guarda cambios
    guardar_peliculas(peliculas)

    # Mensaje final
    console.print(

        # Texto verde
        "[green]✔️ Película actualizada correctamente.[/green]"
    )


# ------------------------------------------------------------
# ELIMINAR PELÍCULA
# ------------------------------------------------------------

# Función para eliminar películas
def eliminar_pelicula() -> None:

    # Importa funciones localmente
    from modules.datos import cargar_funciones

    # Muestra panel
    console.print(

        # Panel rojo
        Panel(

            # Texto
            "[bold red]🗑️ Eliminar Película[/bold red]",

            # Tamaño ajustado
            expand=False
        )
    )

    # Carga películas
    peliculas = cargar_peliculas()

    # Muestra tabla
    mostrar_tabla_peliculas(peliculas)

    # Si no hay películas
    if not peliculas:

        # Sale
        return

    # Manejo de errores
    try:

        # Pide ID
        id_eliminar = IntPrompt.ask(

            # Mensaje
            "  ID de la película a eliminar"
        )

    # Captura error
    except Exception:

        # Mensaje rojo
        console.print("[red]✗ ID inválido.[/red]")

        # Sale
        return

    # Busca película
    pelicula = _buscar_por_id(

        # Lista
        peliculas,

        # ID
        id_eliminar
    )

    # Verifica si existe
    if not pelicula:

        # Mensaje
        console.print(

            # Texto rojo
            f"[red]✗ No existe una película con ID {id_eliminar}.[/red]"
        )

        # Sale
        return

    # Carga funciones del cine
    funciones = cargar_funciones()

    # Busca funciones asociadas
    asociadas = [

        # Recorre funciones
        f for f in funciones

        # Verifica coincidencia
        if f["id_pelicula"] == id_eliminar
    ]

    # Verifica si tiene funciones
    if asociadas:

        # Mensaje de error
        console.print(

            # Texto rojo
            f"[red]✗ No se puede eliminar: la película tiene {len(asociadas)} función(es) registrada(s).[/red]"
        )

        # Sale
        return

    # Pide confirmación
    confirmacion = Prompt.ask(

        # Texto
        f"  ¿Seguro que deseas eliminar '{pelicula['titulo']}'? (s/n)"

    # Convierte a minúscula
    ).lower()

    # Si no escribió s
    if confirmacion != "s":

        # Mensaje amarillo
        console.print("[yellow]Operación cancelada.[/yellow]")

        # Sale
        return

    # Elimina película
    peliculas.remove(pelicula)

    # Guarda cambios
    guardar_peliculas(peliculas)

    # Mensaje verde
    console.print(

        # Texto
        "[green]✔️ Película eliminada correctamente.[/green]"
    )


# ------------------------------------------------------------
# BUSCAR POR GÉNERO
# ------------------------------------------------------------

# Función para buscar películas
def buscar_peliculas_por_genero() -> None:

    # Panel decorativo
    console.print(

        # Panel azul
        Panel(

            # Texto
            "[bold blue]🔍 Buscar por Género[/bold blue]",

            # Ajuste tamaño
            expand=False
        )
    )

    # Pide género
    genero = Prompt.ask(

        # Texto
        "  Ingresa el género a buscar"

    # Convierte a minúscula
    ).strip().lower()

    # Carga películas
    peliculas = cargar_peliculas()

    # Filtra resultados
    resultados = [

        # Recorre películas
        p for p in peliculas

        # Busca coincidencia
        if genero in p["genero"].lower()
    ]

    # Si no hay resultados
    if not resultados:

        # Mensaje amarillo
        console.print(

            # Texto
            f"[yellow]⚠️ No se encontraron películas del género '{genero}'.[/yellow]"
        )

        # Sale
        return

    # Muestra resultados
    mostrar_tabla_peliculas(resultados)


# ------------------------------------------------------------
# MENÚ PRINCIPAL
# ------------------------------------------------------------

# Función principal del menú
def menu_peliculas() -> None:

    # Bucle infinito
    while True:

        # Muestra menú
        console.print(

            # Panel
            Panel(

                # Texto del menú
                "[bold cyan]🎬 Gestión de Películas[/bold cyan]\n\n"
                "  [1] Ver catálogo\n"
                "  [2] Agregar película\n"
                "  [3] Actualizar película\n"
                "  [4] Eliminar película\n"
                "  [5] Buscar por género\n"
                "  [0] Volver al menú principal",

                # Color borde
                border_style="cyan",

                # Tamaño
                expand=False
            )
        )

        # Pide opción
        opcion = Prompt.ask(

            # Texto
            "  Selecciona una opción"

        # Limpia espacios
        ).strip()

        # Si escribe 1
        if opcion == "1":

            # Mostrar películas
            leer_peliculas()

        # Si escribe 2
        elif opcion == "2":

            # Crear película
            crear_pelicula()

        # Si escribe 3
        elif opcion == "3":

            # Actualizar película
            actualizar_pelicula()

        # Si escribe 4
        elif opcion == "4":

            # Eliminar película
            eliminar_pelicula()

        # Si escribe 5
        elif opcion == "5":

            # Buscar por género
            buscar_peliculas_por_genero()

        # Si escribe 0
        elif opcion == "0":

            # Rompe el ciclo y sale
            break

        # Si escribe algo inválido
        else:

            # Mensaje de error
            console.print(

                # Texto rojo
                "[red]✗ Opción inválida.[/red]"
            )