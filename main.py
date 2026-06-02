from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from modules.peliculas import menu_peliculas, buscar_por_genero
from modules.funciones import menu_funciones
from modules.reservas import menu_reservas

console = Console()



# Función para mostrar el reporte de ventas

def reporte_ventas():
    console.print(Panel("[bold cyan]📊  REPORTE DE VENTAS[/bold cyan]", box=box.DOUBLE))

    reservas = menu_reservas()
    funciones = menu_funciones()
    peliculas = menu_peliculas()

    if not reservas:
        console.print("[yellow]⚠ No hay reservas registradas aún.[/yellow]")
        return

    from rich.table import Table

    # Contamos boletos por función
    ventas_por_funcion = {}
    for r in reservas:
        id_f = r["id_funcion"]
        if id_f not in ventas_por_funcion:
            ventas_por_funcion[id_f] = 0
        ventas_por_funcion[id_f] += r["cantidad_boletos"]

    tabla = Table(
        title="📊  REPORTE TOTAL DE VENTAS",
        box=box.ROUNDED,
        header_style="bold green",
        border_style="green"
    )
    tabla.add_column("ID Función",  style="cyan",    justify="center")
    tabla.add_column("Película",    style="white",   justify="left")
    tabla.add_column("Sala",        style="yellow",  justify="center")
    tabla.add_column("Horario",     style="yellow",  justify="center")
    tabla.add_column("Boletos Vendidos", style="bold green", justify="center")
    tabla.add_column("Asientos Libres",  style="magenta",    justify="center")

    total_general = 0
    for id_f, total in ventas_por_funcion.items():
        funcion = funciones.get(id_f, {})
        titulo = peliculas.get(funcion.get("id_pelicula", ""), {}).get("titulo", "N/A")
        sala = funcion.get("sala", "N/A")
        horario = funcion.get("horario", "N/A")
        libres = funcion.get("asientos_disponibles", "?")

        tabla.add_row(id_f, titulo, sala, horario, str(total), str(libres))
        total_general += total

    console.print(tabla)
    console.print(f"\n  [bold]Total de boletos vendidos en todo el cine:[/bold] [bold green]{total_general}[/bold green]")



# Función para mostrar la pantalla de bienvenida

def mostrar_bienvenida():
    console.clear()
    bienvenida = Text()
    bienvenida.append("\n")
    bienvenida.append("  ██████╗██╗███╗   ██╗███████╗\n", style="bold red")
    bienvenida.append("  ██╔════╝██║████╗  ██║██╔════╝\n", style="bold red")
    bienvenida.append("  ██║     ██║██╔██╗ ██║█████╗  \n", style="bold yellow")
    bienvenida.append("  ██║     ██║██║╚██╗██║██╔══╝  \n", style="bold yellow")
    bienvenida.append("  ╚██████╗██║██║ ╚████║███████╗\n", style="bold green")
    bienvenida.append("   ╚═════╝╚═╝╚═╝  ╚═══╝╚══════╝\n", style="bold green")
    bienvenida.append("\n  Sistema de Reservas de Cine\n", style="bold white")

    console.print(Panel(bienvenida, box=box.HEAVY, border_style="red", padding=(1, 4)))
    input("\n  Presiona Enter para continuar...")



# Menú principal del sistema

def menu_principal():
    while True:
        console.clear()
        console.print(Panel(
            "[bold white]1.[/bold white]  🎬  Gestión de Películas\n"
            "[bold white]2.[/bold white]  🎟️   Gestión de Funciones\n"
            "[bold white]3.[/bold white]  🎫  Gestión de Reservas\n"
            "[bold white]4.[/bold white]  🔍  Buscar películas por género\n"
            "[bold white]5.[/bold white]  📊  Reporte de ventas\n"
            "[bold white]0.[/bold white]  🚪  Salir del sistema",
            title="[bold red]🎬  CINE — MENÚ PRINCIPAL[/bold red]",
            box=box.HEAVY,
            border_style="red",
            padding=(1, 4)
        ))

        opcion = input("  Selecciona una opción: ").strip()

        if opcion == "1":
            console.clear()
            menu_peliculas()
        elif opcion == "2":
            console.clear()
            menu_funciones()
        elif opcion == "3":
            console.clear()
            menu_reservas()
        elif opcion == "4":
            console.clear()
            buscar_por_genero()
            input("\n  Presiona Enter para continuar...")
        elif opcion == "5":
            console.clear()
            reporte_ventas()
            input("\n  Presiona Enter para continuar...")
        elif opcion == "0":
            console.print(Panel(
                "[bold yellow]¡Hasta pronto! Gracias por usar el sistema.[/bold yellow]",
                box=box.ROUNDED, border_style="yellow"
            ))
            break
        else:
            console.print("[bold red]✗ Opción inválida. Intenta de nuevo.[/bold red]")
            input("\n  Presiona Enter para continuar...")



# Punto de entrada del programa

if __name__ == "__main__":
    mostrar_bienvenida()
    menu_principal()