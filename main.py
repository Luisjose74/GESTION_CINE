"""main.py — Punto de entrada del Sistema de Reservas para un Cine.
Menú principal con rich.
"""

from rich.console import Console #importar la clase Console de la biblioteca rich para imprimir texto formateado en la consola
from rich.panel import Panel #importar la clase Panel de la biblioteca rich para crear paneles decorativos en la consola
from rich.prompt import Prompt #importar la clase Prompt de la biblioteca rich para solicitar entrada del usuario de forma interactiva
from rich.text import Text #importar la clase Text de la biblioteca rich para crear texto con estilos y colores
from modules.peliculas import menu_peliculas 
from modules.funciones  import menu_funciones
from modules.reservas   import menu_reservas
from modules.comida     import menu_comida
from modules.reportes   import menu_reportes

console = Console()


def mostrar_bienvenida() -> None:
    """Muestra el banner de bienvenida al iniciar la app."""
    bienvenida = Text()
    bienvenida.append("\n  🎬  SISTEMA DE RESERVAS\n", style="bold cyan")
    bienvenida.append("      C I N E M A X\n\n", style="bold yellow")
    bienvenida.append("  Bienvenido al sistema de gestión\n", style="white")
    bienvenida.append("  de películas, funciones y reservas.\n", style="white")
    console.print(Panel(bienvenida, border_style="cyan", expand=False))


def menu_principal() -> None: #definir función para mostrar el menú principal
    """Ciclo principal de la aplicación."""
    mostrar_bienvenida()

    while True:
        console.print(Panel(
            "[bold cyan]🏠  MENÚ PRINCIPAL[/bold cyan]\n\n"
            "  [bold cyan][1][/bold cyan]  🎬  Películas\n"
            "  [bold cyan][2][/bold cyan]  🎟  Funciones\n"
            "  [bold cyan][3][/bold cyan]  🎫  Reservas\n"
            "  [bold cyan][4][/bold cyan]  🍿  Cafetería / Combos\n"
            "  [bold cyan][5][/bold cyan]  📊  Reportes de ventas\n\n"
            "  [bold red][0][/bold red]  🚪  Salir",
            border_style="bright_cyan", expand=False
        ))

        opcion = Prompt.ask("  Selecciona una opción").strip()

        if opcion == "1":
            menu_peliculas()
        elif opcion == "2":
            menu_funciones()
        elif opcion == "3":
            menu_reservas()
        elif opcion == "4":
            menu_comida()
        elif opcion == "5":
            menu_reportes()
        elif opcion == "0":
            console.print(Panel(
                "[bold yellow]¡Hasta pronto! 🎬  Gracias por usar CINEMAX.[/bold yellow]",
                border_style="yellow", expand=False
            ))
            break
        else:
            console.print("[red]✗ Opción inválida. Intenta de nuevo.[/red]")


if __name__ == "__main__":
    menu_principal()