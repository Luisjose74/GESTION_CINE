"""
comida.py — Funcionalidad adicional: Combos de comida (crispetas, bebidas, perros, etc.)
Permite gestionar el menú de combos y agregar pedidos de comida a una reserva.
"""

import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from modules.datos import (
    cargar_combos, guardar_combos,
    cargar_pedidos_comida, guardar_pedidos_comida,
    cargar_reservas
)

console = Console()

# Combos iniciales por defecto (se cargan si el JSON está vacío)
COMBOS_DEFAULT = [
    {"id_combo": 1, "nombre": "Crispetas Pequeñas",  "categoria": "Crispetas", "precio": 20000},
    {"id_combo": 2, "nombre": "Crispetas Medianas",  "categoria": "Crispetas", "precio": 25000},
    {"id_combo": 3, "nombre": "Crispetas Grandes",   "categoria": "Crispetas", "precio": 30000},
    {"id_combo": 4, "nombre": "Combo Familiar",      "categoria": "Combos",    "precio": 35000},
    {"id_combo": 5, "nombre": "Gaseosa 350ml",       "categoria": "Bebidas",   "precio": 5000},
    {"id_combo": 6, "nombre": "Gaseosa 500ml",       "categoria": "Bebidas",   "precio": 7000},
    {"id_combo": 7, "nombre": "Agua Mineral",        "categoria": "Bebidas",   "precio": 4000},
    {"id_combo": 8, "nombre": "Jugo Natural",        "categoria": "Bebidas",   "precio": 6000},
    {"id_combo": 9, "nombre": "Perro Caliente",      "categoria": "Comidas",   "precio": 9000},
    {"id_combo": 10,"nombre": "Nachos con Queso",    "categoria": "Comidas",   "precio": 10000},
    {"id_combo": 11,"nombre": "Combo Pareja",        "categoria": "Combos",    "precio": 28000},
    {"id_combo": 12,"nombre": "Dulces Surtidos",     "categoria": "Dulces",    "precio": 5000},
]

#cargar combos o inicializar con defaults
def _inicializar_combos() -> list: #definir función para cargar combos o inicializar con defaults
    """Carga combos; si el JSON está vacío, inicializa con los combos por defecto."""
    combos = cargar_combos() #cargar combos
    if not combos: #si no hay combos, cargar los combos por defecto y guardarlos
        guardar_combos(COMBOS_DEFAULT) #guardar combos por defecto en el JSON
        return COMBOS_DEFAULT #devolver los combos por defecto
    return combos #devolver los combos cargados del JSON

#generar un nuevo ID de combo
def _generar_id_combo(combos: list) -> int: #definir función para generar un nuevo ID de combo
    if not combos: #si no hay combos
        return 1 #devolver 1
    return max(c["id_combo"] for c in combos) + 1 #devolver el máximo ID de combo + 1

#generar un nuevo ID de pedido
def _generar_id_pedido(pedidos: list) -> int: #definir función para generar un nuevo ID de pedido
    if not pedidos: #si no hay pedidos
        return 1 
    return max(p["id_pedido"] for p in pedidos) + 1


# Mostrar menú de combos 

def mostrar_menu_combos(combos: list) -> None: #definir función para mostrar el menú de combos agrupado por categoría
    """Muestra el menú de combos agrupado por categoría."""
    if not combos: #si no hay combos
        console.print("[yellow]⚠  No hay combos registrados.[/yellow]") #mostrar mensaje
        return #salir de la función

    categorias = {} #crear diccionario para agrupar los combos por categoría
    for c in combos: #recorrer los combos y agruparlos por categoría
        categorias.setdefault(c["categoria"], []).append(c) #agregar el combo a la categoría correspondiente en el diccionario

    for cat, items in categorias.items(): #recorrer las categorías y mostrar los combos de cada categoría en una tabla
        tabla = Table(title=f"🍿  {cat}", border_style="yellow", header_style="bold cyan")
        tabla.add_column("ID",      justify="center", style="bold cyan")
        tabla.add_column("Nombre",  style="bold white")
        tabla.add_column("Precio",  justify="right",  style="green")
        for item in items: #recorrer los combos de la categoría y agregarlos a la tabla
            tabla.add_row(str(item["id_combo"]), item["nombre"], f"${item['precio']:,}") #agregar fila a la tabla con el ID, nombre y precio del combo
        console.print(tabla)


# Pedido de comida 

def hacer_pedido_comida() -> None: #definir función para hacer un pedido de comida asociado a una reserva
    """Permite agregar pedidos de comida asociados a una reserva."""
    console.print(Panel("[bold yellow]🍿  Pedido de Comida[/bold yellow]", expand=False)) 

    reservas = cargar_reservas() #cargar reservas para mostrar al usuario y permitir seleccionar a cuál reserva asociar el pedido de comida
    if not reservas:
        console.print("[red]✗ No hay reservas activas. Primero crea una reserva.[/red]")
        return

    # Mostrar reservas
    tabla_r = Table(title="Reservas activas", border_style="blue", header_style="bold")
    tabla_r.add_column("ID"); tabla_r.add_column("Cliente"); tabla_r.add_column("Asientos")
    for r in reservas: #recorrer las reservas y agregarlas a la tabla para mostrar al usuario
        tabla_r.add_row( #agregar fila a la tabla con el ID de la reserva, nombre del cliente y asientos seleccionados
            str(r["id_reserva"]), #ID de la reserva
            r["nombre_cliente"], #nombre del cliente
            ", ".join(r.get("asientos_seleccionados", [])) #asientos seleccionados (si existen)
        )
    console.print(tabla_r) #mostrar la tabla de reservas activas para que el usuario pueda seleccionar a cuál reserva asociar el pedido de comida

    try: #intentar obtener el ID de la reserva seleccionada por el usuario
        id_reserva = IntPrompt.ask("  ID de la reserva") #pedir al usuario que ingrese el ID de la reserva a la que desea asociar el pedido de comida
    except Exception: #si la entrada es inválida
        console.print("[red]✗ ID inválido.[/red]") #mostrar mensaje de error y salir de la función
        return

    reserva = next((r for r in reservas if r["id_reserva"] == id_reserva), None) 
    #buscar la reserva seleccionada por el usuario en la lista de reservas cargadas, 
    # si no se encuentra, mostrar mensaje de error y salir de la función
    if not reserva:
        console.print("[red]✗ Reserva no encontrada.[/red]")
        return

    combos = _inicializar_combos() #inicializar los combos (cargar del JSON o usar los combos por defecto) 
    #y mostrar el menú de combos para que el usuario pueda seleccionar qué productos agregar al pedido de comida
    mostrar_menu_combos(combos) #mostrar el menú de combos para que el usuario pueda seleccionar qué productos agregar al pedido de comida

    items_pedido = [] #crear una lista para almacenar los items del pedido
    total = 0 #variable para acumular el total del pedido de comida a medida que se van agregando items al pedido

    console.print("\n  [dim]Escribe 0 cuando hayas terminado de agregar items.[/dim]") 
    while True: #bucle para permitir al usuario agregar múltiples items al pedido de comida, hasta que decida terminar (ingresando 0)
        try:
            id_combo = IntPrompt.ask("  ID del combo (0 para terminar)") #pedir al usuario que ingrese el ID del combo que desea agregar al pedido de comida, o 0 para terminar de agregar items
        except Exception: #si la entrada es inválida
            console.print("[red]✗ Entrada inválida.[/red]")
            continue

        if id_combo == 0: #si el usuario ha decidido terminar de agregar items al pedido de comida (ingresando 0), salir del bucle
            break

        combo = next((c for c in combos if c["id_combo"] == id_combo), None) #buscar el combo seleccionado por el usuario en la lista de combos cargados,
        # si no se encuentra, mostrar mensaje de error y continuar con la siguiente iteración del bucle para permitir al usuario intentar ingresar otro ID de combo válido
        if not combo: 
            console.print("[red]✗ Combo no encontrado.[/red]")
            continue

        try:
            cantidad = IntPrompt.ask(f"  Cantidad de '{combo['nombre']}'") #pedir al usuario que ingrese la cantidad de items del combo que desea agregar al pedido de comida
            if cantidad <= 0: # si la cantidad es menor o igual a 0
                raise ValueError #lanzar una excepción para indicar que la cantidad es inválida
        except Exception:   #si la entrada es inválida
            console.print("[red]✗ Cantidad inválida.[/red]")
            continue

        subtotal = combo["precio"] * cantidad #calcular el subtotal del item agregado al pedido de comida
        items_pedido.append({ 
            "id_combo": id_combo,
            "nombre": combo["nombre"],
            "cantidad": cantidad,
            "precio_unitario": combo["precio"],
            "subtotal": subtotal
        })
        total += subtotal
        console.print(f"  [green]✔ Agregado: {cantidad}x {combo['nombre']} — ${subtotal:,}[/green]")

    if not items_pedido: #si no se agregaron items al pedido de comida
        console.print("[yellow]No se agregó ningún item.[/yellow]") #mostrar mensaje y salir de la función
        return

    # Resumen del pedido
    tabla_pedido = Table(title="Resumen del Pedido", border_style="green", header_style="bold") 
    tabla_pedido.add_column("Producto"); tabla_pedido.add_column("Cant.", justify="center")
    tabla_pedido.add_column("Precio unit.", justify="right"); tabla_pedido.add_column("Subtotal", justify="right")
    for item in items_pedido:
        tabla_pedido.add_row(
            item["nombre"],
            str(item["cantidad"]),
            f"${item['precio_unitario']:,}",
            f"${item['subtotal']:,}"
        )
    console.print(tabla_pedido)
    console.print(f"\n  [bold green]TOTAL: ${total:,}[/bold green]\n")

    conf = Prompt.ask("  ¿Confirmar pedido? (s/n)").lower()
    if conf != "s":
        console.print("[yellow]Pedido cancelado.[/yellow]")
        return

    pedidos = cargar_pedidos_comida() #cargar los pedidos de comida existentes para agregar el nuevo pedido a la lista de pedidos y luego guardar la lista actualizada en el JSON
    nuevo_pedido = { 
        "id_pedido": _generar_id_pedido(pedidos),
        "id_reserva": id_reserva,
        "nombre_cliente": reserva["nombre_cliente"],
        "items": items_pedido,
        "total": total,
        "fecha_pedido": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    pedidos.append(nuevo_pedido)
    guardar_pedidos_comida(pedidos)
    console.print(f"[bold green]✔ Pedido #{nuevo_pedido['id_pedido']} guardado. ¡Disfruta tu función![/bold green]")


# Gestión del menú de combos (CRUD) 

def agregar_combo() -> None: 
    """Agrega un nuevo producto al menú."""
    console.print(Panel("[bold cyan]➕  Nuevo Combo/Producto[/bold cyan]", expand=False))
    combos = _inicializar_combos()

    nombre    = Prompt.ask("  Nombre del producto").strip()
    categoria = Prompt.ask("  Categoría (Crispetas / Bebidas / Combos / Comidas / Dulces)").strip()
    try:
        precio = int(Prompt.ask("  Precio").replace(",", "").replace(".", "").strip())
        if precio <= 0:
            raise ValueError
    except ValueError:
        console.print("[red]✗ Precio inválido.[/red]")
        return

    nuevo = {
        "id_combo": _generar_id_combo(combos),
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio
    }
    combos.append(nuevo)
    guardar_combos(combos)
    console.print(f"[green]✔ '{nombre}' agregado al menú con ID {nuevo['id_combo']}.[/green]")


def eliminar_combo() -> None:
    """Elimina un producto del menú."""
    combos = _inicializar_combos()
    mostrar_menu_combos(combos)
    try:
        id_eliminar = IntPrompt.ask("  ID del combo a eliminar")
    except Exception:
        console.print("[red]✗ ID inválido.[/red]")
        return
    combo = next((c for c in combos if c["id_combo"] == id_eliminar), None)
    if not combo:
        console.print("[red]✗ Combo no encontrado.[/red]")
        return
    combos.remove(combo)
    guardar_combos(combos)
    console.print(f"[green]✔ '{combo['nombre']}' eliminado del menú.[/green]")


# ── Reporte de ventas de comida ────────────────────────────

def reporte_ventas_comida() -> None: #definir función para mostrar un resumen de ventas de comida, incluyendo total recaudado y unidades vendidas por producto
    """Muestra un resumen de ventas de comida."""
    console.print(Panel("[bold magenta]📊  Reporte de Ventas — Comida[/bold magenta]", expand=False)) 
    pedidos = cargar_pedidos_comida() #cargar los pedidos de comida para calcular el total recaudado y el conteo de unidades vendidas por producto, y luego mostrar esta información al usuario en un formato legible (tabla y resumen)
    if not pedidos: #si no hay pedidos de comida registrados, mostrar mensaje y salir de la función
        console.print("[yellow]⚠  No hay pedidos de comida registrados.[/yellow]")
        return

    total_general = sum(p["total"] for p in pedidos) #calcular el total recaudado en comida
    conteo_items: dict = {} #crear un diccionario para contar las unidades vendidas por producto, donde la clave es el nombre del producto y el valor es la cantidad total vendida de ese producto

    for pedido in pedidos: #recorrer los pedidos de comida
        for item in pedido["items"]: #
            nombre = item["nombre"]
            conteo_items[nombre] = conteo_items.get(nombre, 0) + item["cantidad"] #agregar la cantidad vendida de ese producto al diccionario

    tabla = Table(title="Ventas por Producto", border_style="magenta", header_style="bold")
    tabla.add_column("Producto"); tabla.add_column("Unidades vendidas", justify="center")
    for nombre, unidades in sorted(conteo_items.items(), key=lambda x: -x[1]):
        tabla.add_row(nombre, str(unidades))
    console.print(tabla)

    console.print(f"\n  [bold green]💰 Total recaudado en comida: ${total_general:,}[/bold green]")
    console.print(f"  [dim]Total pedidos: {len(pedidos)}[/dim]\n")


# Menú

def menu_comida() -> None:
    while True:
        console.print(Panel(
            "[bold yellow]🍿  Cafetería / Combos[/bold yellow]\n\n"
            "  [1] Ver menú de combos\n"
            "  [2] Pedir comida (asociar a reserva)\n"
            "  [3] Agregar producto al menú\n"
            "  [4] Eliminar producto del menú\n"
            "  [5] Reporte de ventas de comida\n"
            "  [0] Volver al menú principal",
            border_style="yellow", expand=False
        ))

        opcion = Prompt.ask("  Selecciona una opción").strip()

        if opcion == "1":
            mostrar_menu_combos(_inicializar_combos())
        elif opcion == "2":
            hacer_pedido_comida()
        elif opcion == "3":
            agregar_combo()
        elif opcion == "4":
            eliminar_combo()
        elif opcion == "5":
            reporte_ventas_comida()
        elif opcion == "0":
            break
        else:
            console.print("[red]✗ Opción inválida.[/red]")
