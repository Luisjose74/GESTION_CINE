# 🎬🍿 Sistema de Reservas para un Cine

> 🎥 Proyecto de **consola** desarrollado en **Python** para gestionar películas en cartelera, funciones de cine, reservas de boletos, combos de comida y reportes de ventas.
> 🎨 Interfaz enriquecida con `rich`, persistencia con CSV y JSON, validaciones estrictas (control de asientos, cupos, stock de comida y selección de butacas) y calidad garantizada con `ruff` y `pytest`.

---

## 📚 Índice

0️⃣ Integrantes  
1️⃣ Descripción general  
2️⃣ Objetivos y alcance  
3️⃣ Entidades y formatos de datos  
4️⃣ Funcionalidades principales  
5️⃣ Estructura del proyecto  
6️⃣ Requisitos e instalación  
7️⃣ Uso — flujo de operación y ejemplos  
8️⃣ Validaciones y reglas de negocio  
9️⃣ Calidad, pruebas y linters  
🔟 Buenas prácticas de Git  
1️⃣1️⃣ Ejemplos de archivos de datos  

---

## 🧑‍💻 0. Integrantes

**Desarrolladores:**

| Rol | Nombre |
|-----|--------|
| 👨‍💻 Developer 1 — **LUIS JOSE SILVA FAJARDO** 
| 👩‍💻 Developer 2 — **GISELLE VANESSA VELASQUEZ ALBARRACIN** 
| 👩‍💻 Developer 3 — **LAURA DANIELA SICUARIZA GOMEZ** 
| 👨‍💻 Developer 4 — **JHON ALEXANDER BARRERO**

**Ficha:** _(3321349)_
**Programa de Formación:** Análisis y Desarrollo de Software
**Centro de Formación:** _(CorpoUne)_

**Instructores:**
- 🧑‍🏫 Instructor 1: Andrés Felipe Sandoval

---

## 🎥 1. Descripción general

Este proyecto es un **Sistema de Reservas para un Cine** de consola que permite:

✅ Administrar **películas en cartelera** y **funciones** (CRUD completo).
✅ **Gestionar reservas de boletos** con validación de cupos disponibles.
✅ **Controlar la selección de asientos** individuales (ej. "A1", "B3").
✅ **Gestionar combos y productos de comida** (crispetas, bebidas, dulces) con control de stock.
✅ **Generar reportes** de ventas, ocupación por función y productos más vendidos.
✅ Mostrar toda la información con tablas y paneles elegantes gracias a `rich`.

> 💡 Diseñado para pequeñas salas de cine o proyectos académicos, con código modular, limpio y testeable.

---

## 🎯 2. Objetivos y alcance

### 🎯 Objetivo general

Desarrollar un sistema modular, validado y testeable que cumpla los requisitos funcionales de gestión de reservas cinematográficas, siguiendo los estándares de calidad exigidos por la guía de laboratorio SENA.

### 🎯 Objetivos específicos

- Registrar y persistir **películas y funciones** en archivos CSV.
- Gestionar **reservas de boletos** en formato JSON.
- Controlar la disponibilidad de asientos por función.
- Prevenir sobreventa: no permitir reservas si la función está llena.
- Implementar selección de asientos específicos (ej. "A1", "A2").
- Administrar el **catálogo de comida y bebidas** con control de stock y precios.
- Generar **reportes de ventas** por función, película y productos más pedidos.
- Mantener estándares de calidad (tipado, docstrings, linters y pruebas unitarias).
- Cumplir con los lineamientos del curso: `pytest`, `ruff`, modularidad y manejo robusto de errores.

---

## 🧾 3. Entidades y formatos de datos

### 🎬 Películas — `peliculas.csv`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_pelicula` | str/int | Identificador único de la película |
| `titulo` | str | Título de la película |
| `genero` | str | Género cinematográfico (Terror, Comedia, Acción…) |
| `duracion_min` | int | Duración en minutos |

#### Ejemplo:
```csv
id_pelicula,titulo,genero,duracion_min
1,El Señor de los Anillos,Fantasía,178
2,Toy Story,Animación,81
3,John Wick,Acción,101
```

---

### 🕐 Funciones — `funciones.csv`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_funcion` | str/int | Identificador único de la función |
| `id_pelicula` | str/int | Referencia al ID de la película |
| `sala` | str | Número o nombre de la sala (ej. "Sala 1") |
| `horario` | str (HH:MM) | Hora de inicio de la función |
| `asientos_disponibles` | int | Cantidad de asientos libres restantes |

#### Ejemplo:
```csv
id_funcion,id_pelicula,sala,horario,asientos_disponibles
1,1,Sala 1,14:00,80
2,2,Sala 2,16:30,60
3,3,Sala 3,19:00,45
```

---

### 🎟️ Reservas — `reservas.json`

| Clave | Tipo | Ejemplo |
|-------|------|---------|
| `id_reserva` | str/int | "1" |
| `nombre_cliente` | str | "Carlos Pérez" |
| `id_funcion` | str/int | "2" |
| `cantidad_boletos` | int | 2 |
| `asientos` | list[str] | ["A1", "A2"] |

#### Ejemplo:
```json
[
  {
    "id_reserva": "1",
    "nombre_cliente": "Carlos Pérez",
    "id_funcion": "2",
    "cantidad_boletos": 2,
    "asientos": ["A1", "A2"]
  },
  {
    "id_reserva": "2",
    "nombre_cliente": "Ana Gómez",
    "id_funcion": "1",
    "cantidad_boletos": 1,
    "asientos": ["B5"]
  }
]
```

---

### 🍿 Comida — `comida.json`

| Clave | Tipo | Descripción |
|-------|------|-------------|
| `id_producto` | str/int | Identificador único del producto |
| `nombre` | str | Nombre del producto (ej. "Crispetas grandes") |
| `categoria` | str | Categoría (Bebida, Snack, Combo, Dulce) |
| `precio` | float | Precio unitario en pesos |
| `stock` | int | Unidades disponibles en inventario |

#### Ejemplo:
```json
[
  {
    "id_producto": "1",
    "nombre": "Crispetas grandes",
    "categoria": "Snack",
    "precio": 12000,
    "stock": 50
  },
  {
    "id_producto": "2",
    "nombre": "Gaseosa 500ml",
    "categoria": "Bebida",
    "precio": 7000,
    "stock": 80
  },
  {
    "id_producto": "3",
    "nombre": "Combo Familiar",
    "categoria": "Combo",
    "precio": 35000,
    "stock": 20
  }
]
```

---

### 📊 Reportes — generados en consola (sin archivo de persistencia)

Los reportes se calculan dinámicamente al momento de consultarlos, cruzando los datos de `reservas.json`, `funciones.csv`, `peliculas.csv` y `comida.json`. No se almacenan en disco; se presentan como tablas `rich` en pantalla.

| Reporte | Descripción |
|---------|-------------|
| Ventas por función | Total de boletos vendidos y valor recaudado por función |
| Ocupación por sala | Porcentaje de asientos ocupados vs. capacidad total |
| Películas más vistas | Ranking de películas ordenadas por boletos vendidos |
| Productos más vendidos | Productos de comida con mayor número de unidades despachadas |
| Ingresos totales | Suma global de boletos + comida vendida |

---

### 🎬 Películas
- Crear, listar, editar y eliminar películas.
- Búsqueda de películas por **género**.

### 🕐 Funciones
- CRUD completo de funciones (asociadas a una película).
- Visualización de funciones disponibles con sus asientos restantes.

### 🎟️ Reservas
- Crear una reserva seleccionando cliente, función y boletos.
- Selección de **asientos específicos** (ej. "A1", "B3") guardados en el JSON.
- Validación de cupos: si la función está llena, no se permite reservar.
- Listar todas las reservas para una función específica.
- Cancelar una reserva (devuelve los asientos al pool disponible).

### 🍿 Comida
- Crear, listar, editar y eliminar productos del catálogo.
- Control de **stock**: se descuenta al asociar productos a una reserva.
- Búsqueda por **categoría** (Bebida, Snack, Combo, Dulce).
- Validación de disponibilidad antes de confirmar el pedido.

### 📊 Reportes
- Ventas totales de boletos por función y por película.
- Porcentaje de **ocupación** por sala.
- Ranking de **películas más vistas**.
- Productos de comida más vendidos.
- Reporte de **ingresos globales** (boletos + comida).

### 🎨 Interfaz visual en consola
- Menús interactivos, tablas y paneles estilizados con `rich`.
- Mensajes de éxito en verde y errores en rojo, con paneles informativos.

---

## 🧱 5. Estructura del proyecto

```
PROYECTO_CINE/
│
├── 📁 Controlador/                    # Lógica de negocio y acceso a datos
│   ├── gestor_peliculas.py            # CRUD de películas (cargar, guardar, listar, buscar)
│   ├── gestor_funciones.py            # CRUD de funciones (crear, listar, actualizar asientos)
│   ├── gestor_reservas.py             # Lógica de reservas (crear, cancelar, listar por función)
│   ├── gestor_comida.py               # CRUD del catálogo de comida y control de stock
│   └── gestor_reportes.py             # Generación de reportes cruzando todas las entidades
│
├── 📁 Modelo/                         # Clases de dominio (entidades del sistema)
│   ├── pelicula.py                    # Clase Pelicula: id, titulo, genero, duracion_min
│   ├── funcion.py                     # Clase Funcion: id, id_pelicula, sala, horario, asientos
│   ├── reserva.py                     # Clase Reserva: id, nombre_cliente, id_funcion, boletos, asientos
│   ├── comida.py                      # Clase Comida: id, nombre, categoria, precio, stock
│   └── reporte.py                     # Clase Reporte: estructuras de datos para resultados de reportes
│
├── 📁 Validaciones/                   # Módulos de validación de entradas y reglas de negocio
│   ├── entrada_datos.py               # Valida tipos de dato, formatos (hora HH:MM, enteros, precios)
│   └── validar_campos.py              # Reglas: cupo disponible, asientos no duplicados, stock suficiente
│
├── 📁 Vista/                          # Presentación en consola con rich
│   ├── vista_principal.py             # Menú principal del sistema
│   ├── vista_pelicula.py              # Submenú y tablas de películas
│   ├── vista_funcion.py               # Submenú y tablas de funciones
│   ├── vista_reserva.py               # Submenú y tablas de reservas
│   ├── vista_asientos.py              # Vista del mapa de asientos por función
│   ├── vista_comida.py                # Submenú y tablas del catálogo de comida
│   └── vista_reportes.py              # Submenú y presentación de reportes con tablas rich
│
├── 📁 data/                           # Archivos de persistencia
│   ├── peliculas.csv                  # Registro de películas en cartelera
│   ├── funciones.csv                  # Registro de funciones programadas
│   ├── reservas.json                  # Registro de reservas realizadas
│   └── comida.json                    # Catálogo de productos de comida con stock y precios
│
├── 📁 tests/                          # Pruebas unitarias con pytest
│   ├── test_peliculas.py              # Tests CRUD de películas
│   ├── test_funciones.py              # Tests CRUD de funciones y control de asientos
│   ├── test_reservas.py               # Tests de reserva: éxito, cupo lleno, cancelación
│   ├── test_comida.py                 # Tests CRUD de comida: stock suficiente, descuento, reposición
│   └── test_reportes.py              # Tests de reportes: cálculos de ventas, ocupación e ingresos
│
├── pyproject.toml                     # Configuración del proyecto (dependencias, ruff, pytest)
├── main.py                            # Punto de entrada de la aplicación
└── README.md                          # Documentación del proyecto
```

### Descripción detallada del árbol

| Carpeta/Archivo | Responsabilidad |
|----------------|-----------------|
| `Controlador/` | Toda la lógica de negocio. Cada archivo gestiona una entidad. Sigue el Principio de Responsabilidad Única. |
| `Modelo/` | Clases Python que representan las entidades del dominio. Sin lógica de negocio, solo estructura de datos. |
| `Validaciones/` | Funciones puras de validación. Se invocan desde los controladores antes de persistir datos. |
| `Vista/` | Maneja exclusivamente la presentación: menús, tablas `rich`, mensajes de error/éxito. |
| `data/` | Archivos de persistencia. Películas y funciones en CSV; reservas en JSON (exigido por la guía). |
| `tests/` | Pruebas unitarias con `pytest`. Cubren CRUD, validaciones y reglas de negocio. |
| `main.py` | Orquesta el arranque: carga datos, muestra el menú principal e inicia el bucle de la aplicación. |
| `pyproject.toml` | Define dependencias (`rich`, `pytest`, `ruff`) y configuración del linter. |

---

## 💻 6. Requisitos e instalación

### 🔧 Requisitos

- Python **3.10** o superior
- Librerías: `rich`, `pytest`, `ruff`

### 🚀 Instalación rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/<tu-usuario>/proyecto_cine.git
cd proyecto_cine

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno virtual
# Windows:
.\.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 4. Instalar dependencias
pip install rich pytest ruff

# 5. Ejecutar la aplicación
python main.py
```

> 💡 También puedes usar `uv` si está disponible:
> ```bash
> uv venv .venv && uv sync && python main.py
> ```

---

## 🧠 7. Uso — flujo de operación y ejemplos

### Menú principal

Al ejecutar `python main.py` verás un panel `rich` con las opciones:

```
╔══════════════════════════════════════╗
║    🎬  SISTEMA DE RESERVAS - CINE    ║
╠══════════════════════════════════════╣
║  1. Gestión de Películas             ║
║  2. Gestión de Funciones             ║
║  3. Gestión de Reservas              ║
║  0. Salir                            ║
╚══════════════════════════════════════╝
```

---

### 🎬 Crear una reserva paso a paso

1️⃣ Selecciona `3. Gestión de Reservas`.
2️⃣ Elige `1. Nueva Reserva`.
3️⃣ Ingresa el nombre del cliente.
4️⃣ Selecciona la función deseada (se muestra tabla de funciones disponibles).
5️⃣ Indica la cantidad de boletos.
6️⃣ Escoge los asientos específicos de la lista disponible (ej. "A1", "B3").

🟢 Si hay cupos → la reserva se guarda en `reservas.json` y los asientos se descuentan.
🔴 Si la función está llena → se notifica al usuario y **no** se guarda la reserva.

---

### 🔍 Buscar película por género

1️⃣ Selecciona `1. Gestión de Películas`.
2️⃣ Elige `5. Buscar por Género`.
3️⃣ Escribe el género (ej. "Acción").
4️⃣ Se muestra una tabla `rich` con todas las coincidencias.

---

## 🧩 8. Validaciones y reglas de negocio

✔️ Validación de formato de hora (`HH:MM`, 24 horas).
✔️ Verificación de que el `id_pelicula` referenciado en una función exista en `peliculas.csv`.
✔️ **Control de cupos**: la reserva se rechaza si `asientos_disponibles < cantidad_boletos`.
✔️ **Control de asientos**: no se permite seleccionar un asiento ya ocupado en la misma función.
✔️ Los asientos seleccionados se listan y validan antes de confirmar la reserva.
✔️ Al cancelar una reserva, los asientos y el cupo se **devuelven** automáticamente a la función.
✔️ Manejo robusto de errores con `try/except` para entradas inválidas y archivos ausentes (`FileNotFoundError`).
✔️ Responsabilidad única por función (Principio SRP).

---

## 🧪 9. Calidad, pruebas y linters

### 🧩 Pruebas unitarias con pytest

```bash
pytest tests/ -v
```

Escenarios cubiertos:

- CRUD completo de películas (crear, leer, actualizar, eliminar).
- CRUD completo de funciones.
- Reserva exitosa con asientos disponibles.
- Rechazo de reserva cuando la función está llena.
- Rechazo de asiento duplicado en la misma función.
- Cancelación de reserva y devolución correcta de cupo.

### 🧹 Linting con Ruff

```bash
ruff check .
```

### 📏 Buenas prácticas aplicadas

- **Type hints** en todas las funciones y métodos.
- **Docstrings** descriptivos en cada función.
- Nombres de variables y funciones coherentes (snake_case).
- Separación clara entre Modelo, Controlador, Vista y Validaciones (patrón MVC simplificado).

---

## 🌿 10. Buenas prácticas de Git

- Mensajes de commit claros, descriptivos y en español.
- Flujo con ramas por funcionalidad.
- Pull Requests con descripción del cambio realizado.

```bash
# Crear rama para nueva funcionalidad
git checkout -b feature/seleccion-asientos

# Agregar cambios
git add .

# Commit con mensaje claro
git commit -m "✨ Implementar selección de asientos por función"

# Subir rama
git push origin feature/seleccion-asientos
```

Ejemplos de mensajes de commit:

| Emoji | Tipo | Ejemplo |
|-------|------|---------|
| ✨ | Nueva funcionalidad | `✨ Agregar búsqueda de películas por género` |
| 🐛 | Corrección de bug | `🐛 Corregir actualización de asientos al cancelar reserva` |
| ✅ | Tests | `✅ Agregar pruebas unitarias para gestor_reservas` |
| 📝 | Documentación | `📝 Actualizar README con ejemplos de uso` |
| ♻️ | Refactoring | `♻️ Extraer validaciones de cupo a módulo independiente` |

---

## 📂 11. Ejemplos de archivos de datos

### 🎬 peliculas.csv
```csv
id_pelicula,titulo,genero,duracion_min
1,El Señor de los Anillos,Fantasía,178
2,Toy Story,Animación,81
3,John Wick,Acción,101
4,El Exorcista,Terror,122
```

### 🕐 funciones.csv
```csv
id_funcion,id_pelicula,sala,horario,asientos_disponibles
1,1,Sala 1,14:00,80
2,2,Sala 2,16:30,60
3,3,Sala 3,19:00,45
4,4,Sala 1,21:00,80
```

### 🎟️ reservas.json
```json
[
  {
    "id_reserva": "1",
    "nombre_cliente": "Carlos Pérez",
    "id_funcion": "2",
    "cantidad_boletos": 2,
    "asientos": ["A1", "A2"]
  },
  {
    "id_reserva": "2",
    "nombre_cliente": "Ana Gómez",
    "id_funcion": "1",
    "cantidad_boletos": 1,
    "asientos": ["B5"]
  }
]
```

---

💛 **¡Gracias por leer!**
Proyecto académico — SENA · Análisis y Desarrollo de Software
Desarrollado con ❤️ y Python 🐍🎬