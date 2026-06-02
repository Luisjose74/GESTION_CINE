from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datos import cargar_funciones, guardar_funciones, cargar_peliculas

console = Console()

# ─────────────────────────────────────────────
# Función para generar un ID único para funciones
# ─────────────────────────────────────────────
def generar_id_funcion(funciones):
    if not funciones:
        return "FUN-001"
    ultimo_id = funciones[-1]["id_funcion"]
    numero = int(ultimo_id.split("-")[1]) + 1
    return f"FUN-{numero:03d}"


# ─────────────────────────────────────────────
# Función para CREAR una nueva función (horario)
# ─────────────────────────────────────────────
def crear_funcion():
    console.print(Panel("[bold cyan]➕  AGREGAR NUEVA FUNCIÓN[/bold cyan]", box=box.DOUBLE))

    peliculas = cargar_peliculas()

    if not peliculas:
        console.print("[bold red]✗ No hay películas registradas. Agrega una película primero.[/bold red]")
        return

    tabla = Table(title="Películas disponibles", box=box.SIMPLE, header_style="bold cyan")
    tabla.add_column("ID",     style="cyan",  justify="center")
    tabla.add_column("Título", style="white", justify="left")
    tabla.add_column("Género", style="green", justify="center")
    for p in peliculas:
        tabla.add_row(p["id_pelicula"], p["titulo"], p["genero"])
    console.print(tabla)

    try:
        id_pelicula = input("  ID de la película para esta función: ").strip().upper()

        pelicula_valida = any(p["id_pelicula"] == id_pelicula for p in peliculas)
        if not pelicula_valida:
            console.print(f"[bold red]✗ No existe una película con ID '{id_pelicula}'.[/bold red]")
            return

        sala = input("  Sala (ej: Sala 1, IMAX, VIP): ").strip()
        if not sala:
            console.print("[bold red]✗ La sala no puede estar vacía.[/bold red]")
            return

        horario = input("  Horario (ej: 2025-06-15 15:30): ").strip()
        if not horario:
            console.print("[bold red]✗ El horario no puede estar vacío.[/bold red]")
            return

        asientos = int(input("  Número de asientos disponibles: "))
        if asientos <= 0:
            console.print("[bold red]✗ Los asientos deben ser mayores a 0.[/bold red]")
            return

    except ValueError:
        console.print("[bold red]✗ Los asientos deben ser un número entero.[/bold red]")
        return

    funciones = cargar_funciones()
    nueva_funcion = {
        "id_funcion": generar_id_funcion(funciones),
        "id_pelicula": id_pelicula,
        "sala": sala,
        "horario": horario,
        "asientos_disponibles": asientos,
        "asientos_totales": asientos,
        "asientos_ocupados": []
    }

    funciones.append(nueva_funcion)
    guardar_funciones(funciones)
    console.print(f"\n[bold green]✔ Función creada con ID: {nueva_funcion['id_funcion']} — {sala} — {horario}[/bold green]")


# ─────────────────────────────────────────────
# Función para LISTAR todas las funciones
# ─────────────────────────────────────────────
def listar_funciones():
    funciones = cargar_funciones()
    peliculas = {p["id_pelicula"]: p for p in cargar_peliculas()}

    if not funciones:
        console.print(Panel("[yellow]⚠ No hay funciones registradas aún.[/yellow]", box=box.ROUNDED))
        return

    tabla = Table(
        title="🎟️  FUNCIONES PROGRAMADAS",
        box=box.ROUNDED,
        header_style="bold cyan",
        border_style="cyan"
    )
    tabla.add_column("ID Función", style="cyan",    justify="center", min_width=10)
    tabla.add_column("Película",   style="white",   justify="left",   min_width=25)
    tabla.add_column("Sala",       style="green",   justify="center", min_width=10)
    tabla.add_column("Horario",    style="yellow",  justify="center", min_width=18)
    tabla.add_column("Asientos",   style="magenta", justify="center", min_width=10)

    for f in funciones:
        titulo_pelicula = peliculas.get(f["id_pelicula"], {}).get("titulo", "Película eliminada")
        asientos_info = f"[green]{f['asientos_disponibles']}[/green]/{f['asientos_totales']}"
        tabla.add_row(f["id_funcion"], titulo_pelicula, f["sala"], f["horario"], asientos_info)

    console.print(tabla)


# ─────────────────────────────────────────────
# Función para ACTUALIZAR una función
# ─────────────────────────────────────────────
def actualizar_funcion():
    console.print(Panel("[bold cyan]✏️  ACTUALIZAR FUNCIÓN[/bold cyan]", box=box.DOUBLE))
    listar_funciones()

    id_buscar = input("\n  ID de la función a modificar: ").strip().upper()
    funciones = cargar_funciones()

    funcion_encontrada = None
    for f in funciones:
        if f["id_funcion"] == id_buscar:
            funcion_encontrada = f
            break

    if not funcion_encontrada:
        console.print(f"[bold red]✗ No se encontró la función '{id_buscar}'.[/bold red]")
        return

    console.print(f"\n  [bold]Función actual:[/bold] Sala: {funcion_encontrada['sala']} | Horario: {funcion_encontrada['horario']}")
    console.print("  [dim](Presiona Enter para mantener el valor actual)[/dim]\n")

    try:
        nueva_sala = input(f"  Nueva sala [{funcion_encontrada['sala']}]: ").strip()
        nuevo_horario = input(f"  Nuevo horario [{funcion_encontrada['horario']}]: ").strip()

        if nueva_sala:
            funcion_encontrada["sala"] = nueva_sala
        if nuevo_horario:
            funcion_encontrada["horario"] = nuevo_horario

    except Exception as e:
        console.print(f"[bold red]✗ Error inesperado: {e}[/bold red]")
        return

    guardar_funciones(funciones)
    console.print(f"\n[bold green]✔ Función '{id_buscar}' actualizada correctamente.[/bold green]")


# ─────────────────────────────────────────────
# Función para ELIMINAR una función
# ─────────────────────────────────────────────
def eliminar_funcion():
    console.print(Panel("[bold red]🗑️  ELIMINAR FUNCIÓN[/bold red]", box=box.DOUBLE))
    listar_funciones()

    id_buscar = input("\n  ID de la función a eliminar: ").strip().upper()
    funciones = cargar_funciones()

    funcion_encontrada = None
    for f in funciones:
        if f["id_funcion"] == id_buscar:
            funcion_encontrada = f
            break

    if not funcion_encontrada:
        console.print(f"[bold red]✗ No se encontró la función '{id_buscar}'.[/bold red]")
        return

    confirmar = input(f"\n  ¿Eliminar la función '{id_buscar}' ({funcion_encontrada['sala']} - {funcion_encontrada['horario']})? (s/n): ").strip().lower()
    if confirmar != "s":
        console.print("[yellow]⚠ Operación cancelada.[/yellow]")
        return

    funciones.remove(funcion_encontrada)
    guardar_funciones(funciones)
    console.print(f"\n[bold green]✔ Función '{id_buscar}' eliminada.[/bold green]")


# ─────────────────────────────────────────────
# Menú principal de funciones
# ─────────────────────────────────────────────
def menu_funciones():
    while True:
        console.print(Panel(
            "[bold white]1.[/bold white] Agregar función\n"
            "[bold white]2.[/bold white] Ver todas las funciones\n"
            "[bold white]3.[/bold white] Actualizar función\n"
            "[bold white]4.[/bold white] Eliminar función\n"
            "[bold white]0.[/bold white] Volver al menú principal",
            title="[bold cyan]🎟️  GESTIÓN DE FUNCIONES[/bold cyan]",
            box=box.ROUNDED,
            border_style="cyan"
        ))

        opcion = input("  Selecciona una opción: ").strip()

        if opcion == "1":
            crear_funcion()
        elif opcion == "2":
            listar_funciones()
        elif opcion == "3":
            actualizar_funcion()
        elif opcion == "4":
            eliminar_funcion()
        elif opcion == "0":
            break
        else:
            console.print("[bold red]✗ Opción inválida. Intenta de nuevo.[/bold red]")

        input("\n  Presiona Enter para continuar...")
        console.clear()