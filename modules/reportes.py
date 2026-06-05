"""
reportes.py — Reto Final: Reporte de ventas del cine.
Muestra el total recaudado, las películas más vistas, funciones más concurridas y más.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from modules.datos import (
    cargar_reservas, cargar_funciones,
    cargar_peliculas, cargar_pedidos_comida
)

console = Console()


def _titulo_pelicula(id_pelicula: int) -> str: #función auxiliar para obtener el título de una película dado su ID
    for p in cargar_peliculas(): #recorre la lista de peliculas
        if p["id_pelicula"] == id_pelicula: #compara el ID de la pelicula
            return p["titulo"] #devuelve el título
    return "Desconocida" #si no encuentra la pelicula devuelve "Desconocida"


def reporte_ventas() -> None: #función principal para generar el reporte de ventas
    console.print(Panel( #imprime un panel con el título del reporte
        "[bold magenta]📊  REPORTE GENERAL DE VENTAS — CINE[/bold magenta]",
        #imprime un panel con el título del reporte
        border_style="magenta", expand=False #el panel no se expande al ancho de la consola, sino que se ajusta al contenido
    ))

    reservas  = cargar_reservas() #carga las reservas
    funciones = cargar_funciones()
    peliculas = cargar_peliculas()
    pedidos_comida = cargar_pedidos_comida()

    if not reservas: #si no hay reservas, muestra un mensaje de advertencia y sale de la función
        console.print("[yellow]⚠  No hay reservas registradas todavía.[/yellow]")
        return

    #1. Resumen general 
    total_boletos = sum(r["cantidad_boletos"] for r in reservas) 
    #calcular el total de boletos vendidos sumando la cantidad de boletos de cada reserva
    total_comida  = sum(p["total"] for p in pedidos_comida)

    console.print(Panel(
        f"  🎟  Total de reservas  : [bold cyan]{len(reservas)}[/bold cyan]\n"
        f"  🪑  Total de boletos   : [bold cyan]{total_boletos}[/bold cyan]\n"
        f"  🍿  Ingresos comida    : [bold green]${total_comida:,}[/bold green]",
        title="Resumen General", border_style="cyan", expand=False
    ))

    #2. Boletos vendidos por función 
    conteo_funciones: dict = {} #diccionario para contar el total de boletos vendidos
    for r in reservas: #recorre cada reserva y suma la cantidad de 
        #boletos vendidos para cada función
        conteo_funciones[r["id_funcion"]] = conteo_funciones.get(r["id_funcion"], 0) + r["cantidad_boletos"]

    tabla_func = Table(title="🎟  Boletos vendidos por Función",border_style="blue",header_style="bold cyan")
    tabla_func.add_column("ID Función",justify="center")
    tabla_func.add_column("Película")
    tabla_func.add_column("Sala")
    tabla_func.add_column("Horario")
    tabla_func.add_column("Boletos vendidos",justify="center",style="bold green")
    tabla_func.add_column("Asientos libres",justify="center",style="yellow")

    funciones_dict = {f["id_funcion"]: f for f in funciones}
    for id_f, boletos in sorted(conteo_funciones.items(), key=lambda x: -x[1]):
        f = funciones_dict.get(id_f)
        if f:
            tabla_func.add_row(
                str(id_f),
                _titulo_pelicula(f["id_pelicula"]),
                f["sala"],
                f["horario"],
                str(boletos),
                str(f.get("asientos_disponibles", "—"))
            )
    console.print(tabla_func)

    #3. Películas más vistas 
    conteo_peliculas: dict = {}
    for id_f, boletos in conteo_funciones.items():
        f = funciones_dict.get(id_f)
        if f:
            titulo = _titulo_pelicula(f["id_pelicula"])
            conteo_peliculas[titulo] = conteo_peliculas.get(titulo, 0) + boletos

    tabla_pel = Table(title="🎬  Películas más vistas", border_style="magenta", header_style="bold")
    tabla_pel.add_column("Película"); tabla_pel.add_column("Total boletos", justify="center", style="bold green")
    for titulo, boletos in sorted(conteo_peliculas.items(), key=lambda x: -x[1]):
        #ordenar las películas por el total de boletos vendidos
        tabla_pel.add_row(titulo, str(boletos)) 
        #agregar una fila a la tabla con el título de la película y el total de boletos vendidos
    console.print(tabla_pel)

    #4. Total general 
    console.print(Panel(
        f"[bold green]💰  TOTAL GENERAL RECAUDADO (Comida): ${total_comida:,}[/bold green]\n"
        f"[dim]Nota: el precio de los boletos no está configurado en este sistema.\n"
        f"Para activarlo, agrega un campo 'precio_boleto' a cada función.[/dim]",
        border_style="green", expand=False
    ))


def menu_reportes() -> None:
    from rich.prompt import Prompt
    while True:
        console.print(Panel(
            "[bold magenta]📊  Reportes[/bold magenta]\n\n"
            "  [1] Reporte general de ventas\n"
            "  [0] Volver al menú principal",
            border_style="magenta", expand=False
        ))
        opcion = Prompt.ask("  Selecciona una opción").strip()
        if opcion == "1":
            reporte_ventas()
        elif opcion == "0":
            break
        else:
            console.print("[red]✗ Opción inválida.[/red]")