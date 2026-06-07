"""
reservas.py — Lógica relacional de Reservas.
Campos: id_reserva, nombre_cliente, id_funcion, cantidad_boletos, asientos_seleccionados, fecha_reserva
Reto Final: selección de asientos específicos (A1, A2, …).
"""
""" instalamos las librerias necesarias:
datetime: para manejar fechas y horas.
rich: para mejorar la presentación en la terminal (tablas, paneles, prompts).
modules.datos: para cargar y guardar datos de reservas, funciones y películas.
"""
import datetime # sirve para manejar fechas y horas, como la fecha de reserva.
from rich.console import Console # sirve 
from rich.table import Table # # para mostrar tablas de datos
from rich.prompt import Prompt, IntPrompt # sirve para solicitar datos al usuario
from rich.panel import Panel # sirve para crear paneles
from modules.datos import ( # sirve para cargar y guardar datos de reservas, funciones y películas.
    cargar_reservas, guardar_reservas,
    cargar_funciones, guardar_funciones,
    cargar_peliculas
)
# ── Configuración ───────────────────────────────────────────
console = Console()#sirve para imprimir en la terminal con formato enriquecido (colores, tablas, paneles, etc.).


# ── Utilidades ─────────────────────────────────────────────
"""Funciones auxiliares para generar IDs, obtener títulos de películas, 
información de funciones y mostrar mapas de asientos, etc."""
def _generar_id(reservas: list) -> int:# Genera un nuevo ID de reserva incrementando el máximo existente.
    if not reservas:
        return 1 
    return max(r["id_reserva"] for r in reservas) + 1


def _titulo_pelicula(id_pelicula: int) -> str:# Obtiene el título de una película dado su ID.
    for p in cargar_peliculas():
        if p["id_pelicula"] == id_pelicula:
            return p["titulo"]
    return "Desconocida"


def _funcion_info(id_funcion: int):#  Obtiene la información completa de una función dado su ID.
    for f in cargar_funciones():
        if f["id_funcion"] == id_funcion:
            return f
    return None
def _generar_asientos_sala() -> list:
    filas = ["A", "B", "C", "D", "E"]
    # Mediante una comprensión de listas, recorre cada fila ("A"-"E") 
    # y para cada una genera columnas del 1 al 6, uniéndolas en texto (f"{fila}{col}").
    return [f"{fila}{col}" for fila in filas for col in range(1, 7)]

"""Muestra un mapa visual de los asientos de la función, 
indicando cuáles están libres y cuáles ocupados."""
def _mostrar_mapa_asientos(funcion: dict) -> None:
    """Muestra un mapa visual de los asientos de la función."""
    todos      = [f"{fila}{col}" for fila in "ABCDE" for col in range(1, 7)]
    ocupados   = set(funcion.get("asientos_ocupados", []))
    console.print("\n  [bold]Mapa de asientos[/bold]   🟩 Libre   🟥 Ocupado\n")
    fila_actual = ""
    linea = "    "
    for asiento in todos:
        if asiento[0] != fila_actual:
            if fila_actual:
                console.print(linea)
            fila_actual = asiento[0]
            linea = f"  {fila_actual}  "
        icono = "[red]🟥[/red]" if asiento in ocupados else "[green]🟩[/green]"
        linea += f"{icono}[dim]{asiento}[/dim]  "
    console.print(linea)
    console.print()


# ── Crear reserva ──────────────────────────────────────────
"""Permite al usuario crear una nueva reserva seleccionando 
asientos específicos para una función con asientos disponibles."""
def crear_reserva() -> None:
    """Crea una nueva reserva seleccionando asientos específicos."""
    console.print(Panel("[bold cyan]🎫  Nueva Reserva[/bold cyan]", expand=False))

    funciones = cargar_funciones()
    funciones_con_espacio = [f for f in funciones if f.get("asientos_disponibles", 0) > 0]

    if not funciones_con_espacio:
        console.print("[red]✗ No hay funciones con asientos disponibles en este momento.[/red]")
        return

    # Mostrar funciones disponibles
    tabla = Table(title="Funciones disponibles", border_style="blue", header_style="bold")
    tabla.add_column("ID");  tabla.add_column("Película");  tabla.add_column("Sala")
    tabla.add_column("Horario"); tabla.add_column("Asientos libres", justify="center")
    for f in funciones_con_espacio:
        tabla.add_row(
            str(f["id_funcion"]),
            _titulo_pelicula(f["id_pelicula"]),
            f["sala"],
            f["horario"],
            str(f.get("asientos_disponibles", 0))
        )
    console.print(tabla)

    try:
        id_funcion = IntPrompt.ask("  ID de la función")
    except Exception:
        console.print("[red]✗ ID inválido.[/red]")
        return


    funciones_todas = cargar_funciones()
    funcion = next((f for f in funciones_todas if f["id_funcion"] == id_funcion), None)
    if not funcion or funcion.get("asientos_disponibles", 0) <= 0:
        console.print("[red]✗ Función no válida o sin disponibilidad.[/red]")
        return

    nombre_cliente = Prompt.ask("  Nombre del cliente").strip()
    if not nombre_cliente:
        console.print("[red]✗ El nombre no puede estar vacío.[/red]")
        return

    # Mostrar mapa y pedir asientos
    _mostrar_mapa_asientos(funcion)

    try:
        cantidad = IntPrompt.ask("  ¿Cuántos boletos deseas reservar?")
        if cantidad <= 0 or cantidad > funcion.get("asientos_disponibles", 0):
            console.print(f"[red]✗ Solo hay {funcion['asientos_disponibles']} asientos disponibles.[/red]")
            return
    except Exception:
        console.print("[red]✗ Cantidad inválida.[/red]")
        return

    ocupados = set(funcion.get("asientos_ocupados", []))
    asientos_elegidos = []

    for i in range(cantidad):
        while True:
            asiento = Prompt.ask(f"  Elige el asiento {i+1}/{cantidad} (ej. A1, B3)").strip().upper()
            todos_posibles = {f"{fila}{col}" for fila in "ABCDE" for col in range(1, 7)}
            if asiento not in todos_posibles:
                console.print("[red]✗ Asiento no válido. Usa formato letra+número (A1-E6).[/red]")
            elif asiento in ocupados or asiento in asientos_elegidos:
                console.print("[red]✗ Ese asiento ya está ocupado. Elige otro.[/red]")
            else:
                asientos_elegidos.append(asiento)
                console.print(f"  [green]✔ Asiento {asiento} reservado.[/green]")
                break

    # Actualizar función
    funcion["asientos_ocupados"] = list(ocupados) + asientos_elegidos
    funcion["asientos_disponibles"] -= cantidad

    reservas = cargar_reservas()
    nueva_reserva = {
        "id_reserva": _generar_id(reservas),
        "nombre_cliente": nombre_cliente,
        "id_funcion": id_funcion,
        "cantidad_boletos": cantidad,
        "asientos_seleccionados": asientos_elegidos,
        "fecha_reserva": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    reservas.append(nueva_reserva)
    guardar_reservas(reservas)
    guardar_funciones(funciones_todas)

    console.print(Panel(
        f"[bold green]✔ ¡Reserva confirmada![/bold green]\n\n"
        f"  Cliente : [bold]{nombre_cliente}[/bold]\n"
        f"  Función : {_titulo_pelicula(funcion['id_pelicula'])} — {funcion['horario']}\n"
        f"  Sala    : {funcion['sala']}\n"
        f"  Asientos: [bold cyan]{', '.join(asientos_elegidos)}[/bold cyan]\n"
        f"  ID Reserva: [bold]{nueva_reserva['id_reserva']}[/bold]",
        border_style="green", expand=False
    ))


# ── Ver reservas de una función ────────────────────────────

def ver_reservas_por_funcion() -> None:
    """Muestra todas las reservas para una función específica."""
    console.print(Panel("[bold blue]📋  Reservas por Función[/bold blue]", expand=False))
    funciones = cargar_funciones()
    if not funciones:
        console.print("[yellow]⚠  No hay funciones registradas.[/yellow]")
        return

    tabla_f = Table(border_style="blue", header_style="bold")
    tabla_f.add_column("ID"); tabla_f.add_column("Película"); tabla_f.add_column("Horario"); tabla_f.add_column("Sala")
    for f in funciones:
        tabla_f.add_row(str(f["id_funcion"]), _titulo_pelicula(f["id_pelicula"]), f["horario"], f["sala"])
    console.print(tabla_f)

    try:
        id_funcion = IntPrompt.ask("  ID de la función")
    except Exception:
        console.print("[red]✗ ID inválido.[/red]")
        return

    funcion = next((f for f in funciones if f["id_funcion"] == id_funcion), None)
    if not funcion:
        console.print("[red]✗ Función no encontrada.[/red]")
        return

    reservas = [r for r in cargar_reservas() if r["id_funcion"] == id_funcion]
    if not reservas:
        console.print("[yellow]⚠  Esta función no tiene reservas aún.[/yellow]")
        return

    tabla = Table(
        title=f"Reservas — {_titulo_pelicula(funcion['id_pelicula'])} | {funcion['horario']} | {funcion['sala']}",
        border_style="cyan", header_style="bold magenta"
    )
    tabla.add_column("ID Reserva", justify="center")
    tabla.add_column("Cliente")
    tabla.add_column("Boletos",   justify="center")
    tabla.add_column("Asientos")
    tabla.add_column("Fecha")

    for r in reservas:
        tabla.add_row(
            str(r["id_reserva"]),
            r["nombre_cliente"],
            str(r["cantidad_boletos"]),
            ", ".join(r.get("asientos_seleccionados", [])),
            r.get("fecha_reserva", "—")
        )
    console.print(tabla)

    # Mostrar mapa de asientos
    _mostrar_mapa_asientos(funcion)


# ── Cancelar reserva ───────────────────────────────────────

def cancelar_reserva() -> None:
    """Cancela una reserva y libera los asientos."""
    console.print(Panel("[bold red]❌  Cancelar Reserva[/bold red]", expand=False))
    reservas = cargar_reservas()
    if not reservas:
        console.print("[yellow]⚠  No hay reservas registradas.[/yellow]")
        return

    tabla = Table(title="Reservas activas", border_style="red", header_style="bold")
    tabla.add_column("ID"); tabla.add_column("Cliente"); tabla.add_column("Función"); tabla.add_column("Asientos")
    for r in reservas:
        f = _funcion_info(r["id_funcion"])
        info = f"{_titulo_pelicula(f['id_pelicula'])} — {f['horario']}" if f else "—"
        tabla.add_row(
            str(r["id_reserva"]),
            r["nombre_cliente"],
            info,
            ", ".join(r.get("asientos_seleccionados", []))
        )
    console.print(tabla)

    try:
        id_cancelar = IntPrompt.ask("  ID de la reserva a cancelar")
    except Exception:
        console.print("[red]✗ ID inválido.[/red]")
        return

    reserva = next((r for r in reservas if r["id_reserva"] == id_cancelar), None)
    if not reserva:
        console.print(f"[red]✗ No existe reserva con ID {id_cancelar}.[/red]")
        return

    conf = Prompt.ask(f"  ¿Cancelar reserva de [bold]{reserva['nombre_cliente']}[/bold]? (s/n)").lower()
    if conf != "s":
        console.print("[yellow]Operación cancelada.[/yellow]")
        return

    # Liberar asientos en la función
    funciones_todas = cargar_funciones()
    funcion = next((f for f in funciones_todas if f["id_funcion"] == reserva["id_funcion"]), None)
    if funcion:
        for asiento in reserva.get("asientos_seleccionados", []):
            if asiento in funcion["asientos_ocupados"]:
                funcion["asientos_ocupados"].remove(asiento)
        funcion["asientos_disponibles"] += reserva["cantidad_boletos"]
        guardar_funciones(funciones_todas)

    reservas.remove(reserva)
    guardar_reservas(reservas)
    console.print("[green]✔ Reserva cancelada y asientos liberados.[/green]")


# ── Historial por cliente ──────────────────────────────────

def historial_cliente() -> None:
    """Muestra el historial de reservas de un cliente."""
    console.print(Panel("[bold blue]👤  Historial de Cliente[/bold blue]", expand=False))
    nombre = Prompt.ask("  Nombre del cliente").strip().lower()
    reservas = [r for r in cargar_reservas() if nombre in r["nombre_cliente"].lower()]

    if not reservas:
        console.print("[yellow]⚠  No se encontraron reservas para ese cliente.[/yellow]")
        return

    tabla = Table(title=f"Historial de reservas — '{nombre}'", border_style="blue", header_style="bold")
    tabla.add_column("ID", justify="center"); tabla.add_column("Película")
    tabla.add_column("Sala"); tabla.add_column("Horario"); tabla.add_column("Asientos"); tabla.add_column("Fecha")

    for r in reservas:
        f = _funcion_info(r["id_funcion"])
        if f:
            tabla.add_row(
                str(r["id_reserva"]),
                _titulo_pelicula(f["id_pelicula"]),
                f["sala"], f["horario"],
                ", ".join(r.get("asientos_seleccionados", [])),
                r.get("fecha_reserva", "—")
            )
    console.print(tabla)


# ── Menú ───────────────────────────────────────────────────

def menu_reservas() -> None:
    while True:
        console.print(Panel(
            "[bold green]🎫  Gestión de Reservas[/bold green]\n\n"
            "  [1] Ver reservas de una función\n"
            "  [2] Crear nueva reserva\n"
            "  [3] Cancelar reserva\n"
            "  [4] Historial por cliente\n"
            "  [0] Volver al menú principal",
            border_style="green", expand=False
        ))

        opcion = Prompt.ask("  Selecciona una opción").strip()

        if opcion == "1":
            ver_reservas_por_funcion()
        elif opcion == "2":
            crear_reserva()
        elif opcion == "3":
            cancelar_reserva()
        elif opcion == "4":
            historial_cliente()
        elif opcion == "0":
            break
        else:
            console.print("[red]✗ Opción inválida.[/red]")
