# Librerías para mostrar información en consola con formato visual

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel

# Funciones para cargar y guardar datos en archivos JSON
from modules.datos import cargar_funciones, guardar_funciones, cargar_peliculas

# Objeto principal para imprimir información en consola
console = Console()

# Capacidad máxima de cada sala
TOTAL_ASIENTOS_POR_SALA = 30  # Cada sala tiene 30 asientos (A1-E6)



#Genera automáticamente un nuevo ID para una función.

def _generar_id(funciones: list) -> int:
    #Si no existen funciones registradas, comienza en 1.
    if not funciones:
        return 1
    #Si existen, toma el ID más alto y suma 1.
    return max(f["id_funcion"] for f in funciones) + 1


# Busca una función según su ID.
def _buscar_por_id(funciones: list, id_funcion: int):
    #- El diccionario de la función si la encuentra.
    for f in funciones:
        if f["id_funcion"] == id_funcion:
            return f
    #None si no existe.
    return None


def _titulo_pelicula(id_pelicula: int) -> str:
    # Carga todas las películas guardadas en el sistema json
    peliculas = cargar_peliculas()
     # Recorre una por una todas las películas almacenadas
    for p in peliculas:
        if p["id_pelicula"] == id_pelicula:
            return p["titulo"]
    return "Desconocida"


def _generar_asientos_sala() -> list:
    filas = ["A", "B", "C", "D", "E"]
    # Mediante una comprensión de listas, recorre cada fila ("A"-"E") 
    # y para cada una genera columnas del 1 al 6, uniéndolas en texto (f"{fila}{col}").
    return [f"{fila}{col}" for fila in filas for col in range(1, 7)]



def mostrar_tabla_funciones(funciones: list) -> None:
    #Imprime un mensaje de advertencia
    if not funciones:
        console.print("[yellow]⚠  No hay funciones registradas.[/yellow]")
        # Cancela la creación de la función 
        return

    #Se define el nombre, color y alineación de cada columna
    tabla = Table(title="🎟  Funciones Programadas", border_style="magenta", header_style="bold cyan")
    tabla.add_column("ID",         style="bold cyan",   justify="center")
    tabla.add_column("Película",   style="bold white")
    tabla.add_column("Sala",       style="yellow",      justify="center")
    tabla.add_column("Horario",    style="green",       justify="center")
    tabla.add_column("Disponibles",style="bold green",  justify="center")
    tabla.add_column("Capacidad",  style="white",       justify="center")


    #Recorre la lista de funciones
    for f in funciones:
        # Obtiene el nombre de la película asociada a la función
        titulo = _titulo_pelicula(f["id_pelicula"])

        #diccionario.get( "lo_que_busco" , "lo_que_devuelves_si_no_lo_encuentras" )
        # Obtiene la cantidad de asientos libres de la función.
        # Si ese dato no existe en el archivo JSON, asume que hay 30 asientos disponibles.
        disponibles = f.get("asientos_disponibles", TOTAL_ASIENTOS_POR_SALA)

        # Agrega una nueva fila a la tabla con la información de la función actual
        tabla.add_row(
            str(f["id_funcion"]),
            titulo,
            f["sala"],
            f["horario"],
            str(disponibles),
            str(TOTAL_ASIENTOS_POR_SALA)
        )
    # Muestra en pantalla la tabla completa con todas las funciones registradas
    console.print(tabla)

# Función encargada de registrar una nueva función de cine
def crear_funcion():

    console.print(Panel("[bold cyan]➕  Nueva Función[/bold cyan]", expand=False))

    # Carga todas las películas registradas
    peliculas = cargar_peliculas()
    if not peliculas:
         # Verifica si existen películas registradas
        console.print("[red]✗ Primero debes registrar al menos una película.[/red]")
        return

    # Mostrar películas disponibles
    # Crea una tabla para mostrar las películas disponibles
    tabla = Table(title="Películas disponibles", border_style="blue", header_style="bold")
    
    # Agrega las columnas que tendrá la tabla
    tabla.add_column("ID"); tabla.add_column("Título"); tabla.add_column("Género")
    
    # Recorre todas las películas registradas
    for p in peliculas:
        # Agrega cada película como una fila de la tabla
        tabla.add_row(str(p["id_pelicula"]), p["titulo"], p["genero"])
    console.print(tabla)

    try: 
    # Solicita al usuario el ID de la película
    #obliga a que el usuario escriba única y exclusivamente un número entero.
        id_pelicula = IntPrompt.ask("  ID de la película")
    except Exception:
        # Se ejecuta si el usuario ingresa un dato inválido
        console.print("[red]✗ ID inválido.[/red]")
        return
    

    #Si NO existe ninguna película con ese ID
    if not any(p["id_pelicula"] == id_pelicula for p in peliculas):
        console.print(f"[red]✗ No existe película con ID {id_pelicula}.[/red]")
        return

    #Solicita al usuario el nombre o número de la sala
    sala    = Prompt.ask("  Número o nombre de sala (ej. Sala 1, IMAX)").strip()
    # Solicita la fecha y hora en que se realizará la función
    horario = Prompt.ask("  Horario (ej. 2025-07-10 18:00)").strip()

    # Verifica que el usuario no haya dejado los campos vacíos
    if not sala or not horario:
        console.print("[red]✗ Sala y horario son obligatorios.[/red]")
        # Cancela la creación de la función
        return
    
    # Carga desde el JSON todas las funciones que ya existen
    funciones = cargar_funciones()
    # CREAR EL DICCIONARIO (JSON): Estructura los datos de la nueva función de cine
    nueva = {
        #Llama a una función para calcular un número de ID único que no se repita
        "id_funcion": _generar_id(funciones),
        "id_pelicula": id_pelicula,
        "sala": sala,
        "horario": horario,
        "asientos_disponibles": TOTAL_ASIENTOS_POR_SALA,
        "asientos_ocupados": []
    }
    #actualizar la lista Agrega el nuevo diccionario ("nueva")
    funciones.append(nueva)
    #Guardar en disco: Reescribe el archivo JSON con la lista actualizada
    guardar_funciones(funciones)
    #Muestra aviso confirmando el ID y la capacidad de la función creada
    console.print(f"[green]✔ Función creada con ID {nueva['id_funcion']} — {TOTAL_ASIENTOS_POR_SALA} asientos disponibles.[/green]")

# Función que muestra todas las funciones registradas en el sistema
def leer_funciones() -> None:
     # Carga desde el archivo JSON la lista de funciones guardadas
    funciones = cargar_funciones()
    # Llama a la función que muestra en una tabla
    mostrar_tabla_funciones(funciones)


# Función que permite modificar la información de una función existente
def actualizar_funcion() -> None:
    """Actualiza los datos de una función."""
    console.print(Panel("[bold yellow]✏  Actualizar Función[/bold yellow]", expand=False))#Haz el cuadro del tamaño justo del texto
    #Carga todas las funciones y las muestra en una tabla para que el usuario elija cuál editar
    funciones = cargar_funciones()
    mostrar_tabla_funciones(funciones)

    # Si no hay funciones registradas en el sistema, se sale de inmediato
    if not funciones:
        return

    try:#Pide el ID de la función asegurando que sea un número entero
        id_buscar = IntPrompt.ask("  ID de la función a actualizar")
    except Exception:
        console.print("[red]✗ ID inválido.[/red]")
        return

    #Si la función no existe (ej. buscó la 99 pero solo hay 1, 2, 3), avisa y cancela
    funcion = _buscar_por_id(funciones, id_buscar)
    if not funcion:
        console.print(f"[red]✗ No existe una función con ID {id_buscar}.[/red]")
        return
    
    #CAMBIO DE DATOS:
    console.print("  (Deja en blanco para no cambiar el campo)")
    nueva_sala    = Prompt.ask("  Nueva sala",    default=funcion["sala"]).strip()
    nuevo_horario = Prompt.ask("  Nuevo horario", default=funcion["horario"]).strip()

    #Sobreescribe los datos viejos del diccionario con los nuevos
    funcion["sala"]    = nueva_sala
    funcion["horario"] = nuevo_horario

    #Guarda la lista de funciones actualizada en el archivo JSON
    guardar_funciones(funciones)
    console.print("[green]✔ Función actualizada correctamente.[/green]")


def eliminar_funcion() -> None:
    #Trae la herramienta para leer las reservas hechas por los clientes
    from modules.datos import cargar_reservas
    #muestra el titulo
    console.print(Panel("[bold red]🗑  Eliminar Función[/bold red]", expand=False))
    #Carga todas las funciones almacenadas en el JSON
    funciones = cargar_funciones()
     # Muestra las funciones disponibles
    mostrar_tabla_funciones(funciones)

     # Si no existen funciones, termina la ejecución
    if not funciones:
        return

    try:## Solicita el ID de la función que se desea eliminar
        id_eliminar = IntPrompt.ask("  ID de la función a eliminar")
    except Exception:
        console.print("[red]✗ ID inválido.[/red]")
        return

    #Verifica si el ID que pusieron realmente existe en nuestra lista
    funcion = _buscar_por_id(funciones, id_eliminar)
    if not funcion:
        console.print(f"[red]✗ No existe función con ID {id_eliminar}.[/red]")
        return

    reservas = cargar_reservas()
    # Busca las reservas que pertenecen a la función
    # que se intenta eliminar
    #Si encuentras una reserva de esta función, guárdame todo el diccionario de la reserva completo
    asociadas = [r for r in reservas if r["id_funcion"] == id_eliminar]
    if asociadas:
        console.print(f"[red]✗ No se puede eliminar: la función tiene {len(asociadas)} reserva(s) activa(s).[/red]")
        return

    # Solicita una confirmación antes de eliminar
    conf = Prompt.ask(f"  ¿Eliminar función ID {id_eliminar}? (s/n)").lower()
    ## Si el usuario no escribe "s", cancela la operación
    if conf != "s":
        console.print("[yellow]Cancelado.[/yellow]")
        return
    ## Elimina la función de la lista y guarda los cambios en el JSON
    funciones.remove(funcion)
    guardar_funciones(funciones)
    console.print("[green]✔ Función eliminada.[/green]")


# Menú principal para gestionar las funciones del cine
def menu_funciones() -> None:
    while True:
        # Muestra las opciones disponibles del menú
        console.print(Panel(
            "[bold magenta]🎟  Gestión de Funciones[/bold magenta]\n\n"
            "  [1] Ver funciones\n"
            "  [2] Agregar función\n"
            "  [3] Actualizar función\n"
            "  [4] Eliminar función\n"
            "  [0] Volver al menú principal",
            border_style="magenta", expand=False
        ))

        # Solicita al usuario que seleccione una opción
        opcion = Prompt.ask("  Selecciona una opción").strip()

        if opcion == "1":
            leer_funciones()
        elif opcion == "2":
            crear_funcion()
        elif opcion == "3":
            actualizar_funcion()
        elif opcion == "4":
            eliminar_funcion()
        elif opcion == "0":
            break
        else:
            console.print("[red]✗ Opción inválida.[/red]")