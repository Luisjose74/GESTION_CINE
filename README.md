# 🎬🍿 Sistema de Reservas para un Cine

> 🎥 Proyecto de **consola** desarrollado en **Python** para gestionar películas en cartelera, funciones de cine, reservas de boletos, combos de comida y reportes de ventas.
> 🎨 Interfaz enriquecida con `rich`, persistencia con CSV y JSON, validaciones estrictas (control de asientos, cupos, stock de comida y selección de butacas) y calidad garantizada con `ruff` y `pytest`.

---

## 📚 Índice

0️⃣ Integrantes  
1️⃣ Descripción general  
2️⃣ Objetivos  
3️⃣ Entidades y formatos de datos  
4️⃣ Funcionalidades principales  
5️⃣ Estructura del proyecto  
6️⃣ Requisitos e instalación  
7️⃣ Uso — flujo de operación y ejemplos  
8️⃣ Validaciones y reglas de negocio  
9️⃣ Buenas prácticas de Git  
🔟 Ejemplos de archivos de datos  

---

## 🧑‍💻 0. Integrantes

**Desarrolladores:**

| Rol             | Nombre                                             
|-----------------|----------------------------------------|
| 👨‍💻 Developer 1 |— **LUIS JOSE SILVA FAJARDO** |
| 👩‍💻 Developer 2 |— **GISELLE VANESSA VELASQUEZ ALBARRACIN**| 
| 👩‍💻 Developer 3 |— **LAURA DANIELA SICUARIZA GOMEZ** |
| 👨‍💻 Developer 4 |— **JHON ALEXANDER BARRERO**|

**Ficha:** _(3321349)_
**Programa de Formación:** Análisis y Desarrollo de Software
**Centro de Formación:** _(CorpoUne)_

**Instructores:**
- 🧑‍🏫 Instructor: Andrés Felipe Sandoval

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

## 🎯 2. Objetivos 

### 🎯 Objetivo general

Desarrollar un sistema modular, validado y testeable que cumpla los requisitos funcionales de gestión de reservas cinematográficas, siguiendo los estándares de calidad exigidos por la guía de laboratorio SENA.

### 🎯 Objetivos específicos

- Registrar **películas y funciones** en archivos.
- Gestionar **reservas de boletos** en formato JSON.
- Controlar la disponibilidad de asientos por función.
- Prevenir sobreventa: no permitir reservas si la función está llena.
- Implementar selección de asientos específicos (ej. "A1", "A2").
- Administrar el **catálogo de comida y bebidas** con control de stock y precios.
- Generar **reportes de ventas** por función, película y productos más pedidos.

---

## 🧾 3. Entidades y formatos de datos

### 🎬 Películas

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_pelicula` | int | Identificador único de la película |
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

### 🕐 Funciones

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_funcion` | str/int | Identificador único de la función |
| `id_pelicula` | int | Referencia al ID de la película |
| `sala` | str | Número o nombre de la sala (ej. "Sala 1") |
| `horario` | str (HH:MM) | Dia y hora de inicio de la función |
| `asientos_disponibles` | int | Cantidad de asientos libres restantes |

#### Ejemplo:
```
id_funcion,id_pelicula,sala,horario,asientos_disponibles
1,1,Sala 1, 2026-6-1, 14:00:40

```

---

### 🎟️ Reservas 

| Clave | Tipo | Ejemplo |
|-------|------|---------|
| `id_reserva` | int | "1" |
| `nombre_cliente` | str | "Carlos Pérez" |
| `id_funcion` | int | "2" |
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

### 🍿 Comida

| Clave | Tipo | Descripción |
|-------|------|-------------|
| `id_producto` | int | Identificador único del producto |
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
## 4. Funcionalidades principales

### 📊 Reportes — generados en consola

Los reportes se calculan dinámicamente al momento de consultarlos, cruzando los datos de `reservas`, `funciones`, `peliculas` y `comida`. No se almacenan en disco; se presentan como tablas `rich` en pantalla.

| Reporte | Descripción |
|---------|-------------|
| Ventas por función | Total de boletos vendidos y valor recaudado por función |
| Ocupación por sala | porentaje de asientos ocupados - capacidad total |
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
- Selección de **asientos específicos** (ej. "A1", "B3").
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
- **ocupación** por sala.
- Ranking de **películas más vistas**.
- Productos de comida más vendidos.
- Reporte de **ingresos globales** (boletos + comida).

### 🎨 Interfaz visual en consola
- Menús interactivos, tablas y paneles estilizados con `rich`.
- Mensajes de éxito en verde y errores en rojo, con paneles informativos.

---

## 🧱 5. Estructura del proyecto

```
GESTION_CINE/
│
├── 📁 DATA/                    
│   ├── comida.json            
│   ├── funciones.json           
│   ├── reservas.json             
│   ├── peliculas.json               
│   └── reportes.json             
│
├── 📁 Modules/                         
│   ├── pelicula.py                    
│   ├── funciones.py                     
│   ├── reservas.py                     
│   ├── comida.py                      
│   └── reporte.py
│   └── datos.py                     
│                  
├── .gitignore                     
├── main.py    
├── requirements.txt                          
└── README.md                          
```

### Descripción detallada del árbol

| Carpeta/Archivo    | Responsabilidad                                                                      |
| ------------------ | ------------------------------------------------------------------------------------ |
| `DATA/`            | Almacena los archivos JSON utilizados para la persistencia de datos del sistema.     |
| `Modules/`         | Contiene la lógica de negocio. Cada módulo gestiona una entidad específica del cine. |
| `pelicula.py`      | Administración de películas.                                                         |
| `funciones.py`     | Gestión de funciones y horarios.                                                     |
| `reservas.py`      | Registro y control de reservas.                                                      |
| `comida.py`        | Gestión de productos de comida y bebidas.                                            |
| `reporte.py`       | Generación de reportes del sistema.                                                  |
| `datos.py`         | Lectura y escritura de archivos JSON.                                                |
| `.gitignore`       | Archivos y carpetas excluidos del control de versiones.                              |
| `main.py`          | Punto de entrada y ejecución de la aplicación.                                       |
| `requirements.txt` | Dependencias necesarias para ejecutar el proyecto.                                   |
| `README.md`        | Documentación general del sistema.                                                   |


---

## 💻 6. Requisitos e instalación

### 🔧 Requisitos

- Python **3.10** o superior
- Librerías: `rich`

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


# 4. Instalar dependencias
pip install rich 

# 5. Ejecutar la aplicación
python main.py
```


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

✔️ Verificación de que el `id_pelicula` referenciado en una función exista en `peliculas`.
✔️ **Control de cupos**: la reserva se rechaza si `asientos_disponibles < cantidad_boletos`.
✔️ **Control de asientos**: no se permite seleccionar un asiento ya ocupado en la misma función.
✔️ Los asientos seleccionados se listan y validan antes de confirmar la reserva.


## 🌿 9. Buenas prácticas de Git

- Mensajes de commit claros, y descriptivos.

Ejemplos de mensajes de commit:

| Emoji | Tipo | Ejemplo |
|-------|------|---------|
| ✨ | Nueva funcionalidad | `✨ Agregar búsqueda de películas por género` |
| 🐛 | Corrección de bug | `🐛 Corregir actualización de asientos al cancelar reserva` |
| ✅ | Tests | `✅ Agregar pruebas unitarias para gestor_reservas` |
| 📝 | Documentación | `📝 Actualizar README con ejemplos de uso` |
| ♻️ | Refactoring | `♻️ Extraer validaciones de cupo a módulo independiente` |

---

## 📂 10. Ejemplos de archivos de datos

### 🎬 peliculas
```
id_pelicula,titulo,genero,duracion_min
1,El Señor de los Anillos,Fantasía,178
2,Toy Story,Animación,81
3,John Wick,Acción,101
4,El Exorcista,Terror,122
```

### 🕐 funciones
```
id_funcion,id_pelicula,sala,horario,asientos_disponibles
1,1,Sala 1,14:00,80
2,2,Sala 2,16:30,60
3,3,Sala 3,19:00,45
4,4,Sala 1,21:00,80
```

### 🎟️ reservas.json
```
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
Proyecto académico  Grupo 1 — SENA · Análisis y Desarrollo de Software
Desarrollado con ❤️ y Python 🐍🎬