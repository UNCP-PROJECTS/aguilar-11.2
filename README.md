# UNCP — Facultad de Ingeniería de Sistemas
## Desarrollo de Aplicaciones Web (IS093A) &bull; 2026-II
### Guía Práctica Grupal Semana 11: Catálogo de Productos Tecnológicos (Django MTV)

**Integrantes del Equipo:**
- **José Pablo Osorio Mallqui** (Código: `2022200839H`) — *Roles: Arquitecto Django & QA / ORM Validator*
- **Arlette D'Alessandra Suárez Román** (Código: `2022200427L`) — *Roles: Desarrolladora de Vistas & Ingeniera de Plantillas*

**Docente:** Ing. Miguel Aguilar  
**Marco de Trabajo:** DreamDev & DreamDesign (Tema Claro)

---

## 1. Descripción del Proyecto

Implementación de un sistema web modular en **Django 5.x** bajo el patrón de diseño arquitectónico **MTV (Model-Template-View)**. El sistema ofrece un catálogo tecnológico responsivo en **Tema Claro**, enrutamiento desacoplado con resolución de nombres reversibles (`app_name = 'catalogo'`), vistas híbridas (**FBV** para la bienvenida y métricas del sistema, y **CBV ListView** para la navegación paginada y filtrable del catálogo), persistencia relacional con el **ORM de Django** sobre SQLite y un conjunto de pruebas unitarias automatizadas (TDD).

---

## 2. Diagrama del Flujo Arquitectónico MTV

El patrón MTV de Django desacopla responsabilidades delegando el ciclo solicitud-respuesta según el siguiente flujo de ejecución:

```text
  [ Cliente / Navegador Web ]
               │
               ▼  (1) HTTP GET Request (ej. /catalogo/?categoria=Periféricos)
  ┌─────────────────────────────────────────────────────────────┐
  │ 1. URLs Dispatcher                                          │
  │    config/urls.py  ──include()──>  catalogo/urls.py         │
  └────────────────────────────┬────────────────────────────────┘
                               │
                               ▼  (2) Despacho de vista resuelta
  ┌─────────────────────────────────────────────────────────────┐
  │ 2. Capa de Vista (Views)                                    │
  │    catalogo/views.py  [FBV home | CBV ProductoListView]     │
  └──────────────┬──────────────────────────────▲───────────────┘
                 │                              │
     (3) QuerySet│                  (4) Entidades│
        Lazy eval│                     Python   │
                 ▼                              │
  ┌────────────────────────────┐                │
  │ 3. Capa de Modelo (ORM)    │                │
  │    catalogo/models.py      ├────────────────┘
  │    Producto (SQLite DB)    │
  └────────────────────────────┘
                 │
                 ▼  (5) Contexto inyectado (dict: 'productos', 'categorias')
  ┌─────────────────────────────────────────────────────────────┐
  │ 4. Motor de Templates (DTL)                                 │
  │    base.html (Herencia DRY)  <──  catalogo.html             │
  └────────────────────────────┬────────────────────────────────┘
                               │
                               ▼  (6) HTTP Response 200 OK (HTML renderizado)
  [ Cliente / Navegador Web ]
```

---

## 3. Demostración de QuerySets y Lazy Evaluation

En el ORM de Django, los **QuerySets son perezosos (Lazy Evaluation)**: la declaración de una consulta no interactúa inmediatamente con la base de datos relacional. La sentencia SQL solo se compila y ejecuta cuando se requiere evaluar los resultados reales (al iterar en un bucle `for`, llamar a `list()`, `len()` o acceder por índice).

### QuerySet 1: Filtrado de Productos Disponibles Ordenados por Precio
```python
# Consulta diferida (No emite SQL al crearse):
qs_disponibles = Producto.objects.filter(stock__gt=0).order_by('precio')

# Se evalúa en la plantilla DTL al iterar sobre la lista de productos:
# {% for producto in productos %} ... {% endfor %}
```

### QuerySet 2: Agrupación y Listado Único de Categorías para Filtrado
```python
# Extracción de valores escalares únicos diferida en memoria:
qs_categorias = Producto.objects.values_list('categoria', flat=True).distinct()

# Se evalúa cuando la vista inyecta los filtros en el contexto y el template los recorre.
```

---

## 4. Estructura de Directorios del Proyecto

```text
proyecto/
├── assets/                          # Capturas requeridas de /catalogo/ y terminales
│   ├── interfaz_home_fbv.png
│   ├── interfaz_catalogo_cbv.png
│   └── interfaz_catalogo_filtrado.png
├── catalogo/                        # Aplicación de dominio MTV
│   ├── migrations/                  # Historial de migraciones ORM
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── admin.py                     # Panel de administración Django
│   ├── apps.py                      # Configuración de la aplicación
│   ├── models.py                    # Modelo ORM Producto (POO)
│   ├── tests.py                     # Suite de pruebas unitarias automatizadas
│   ├── urls.py                      # Enrutador desacoplado (app_name='catalogo')
│   ├── views.py                     # FBV (home) y CBV (ProductoListView)
│   └── __init__.py
├── config/                          # Configuración raíz de Django
│   ├── settings.py                  # Variables de configuración, apps y templates
│   ├── urls.py                      # Enrutador principal con include()
│   ├── wsgi.py                      # Punto de entrada WSGI
│   └── asgi.py                      # Punto de entrada ASGI
├── static/                          # Archivos estáticos institucionales
│   └── img/logo-uncp.png
├── templates/                       # Plantillas DTL en Tema Claro (DreamDesign)
│   ├── base.html                    # Shell institucional con navegación
│   ├── catalogo.html                # Catálogo con filtros y estados de stock (CBV)
│   └── home.html                    # Bienvenida y métricas (FBV)
├── .gitignore                       # Exclusión de .venv, db.sqlite3 y temporales
├── capture_browser.py               # Conector a Chromium/Chrome con Playwright
├── generate_evidence.py             # Generador de capturas CodeSnap con Pygments
├── manage.py                        # Orquestador CLI de Django
├── poblar_datos.py                  # Seeder de datos reales y verificación Lazy
└── requirements.txt                 # Manifiesto de dependencias
```

---

## 5. Capturas de la Interfaz Renderizada (/catalogo/)

### 5.1. Catálogo Completo Renderizado (CBV ListView en Tema Claro)
![Catálogo Renderizado](assets/interfaz_catalogo_cbv.png)

### 5.2. Catálogo con Filtro Dinámico de Categoría
![Catálogo Filtrado](assets/interfaz_catalogo_filtrado.png)

### 5.3. Página de Inicio y Métricas (FBV en Tema Claro)
![Página de Inicio](assets/interfaz_home_fbv.png)

---

## 6. Instalación y Validación Técnica

### 1. Clonar y Acceder
```powershell
git clone <URL_DEL_REPOSITORIO>
cd proyecto
```

### 2. Crear y Activar Entorno Virtual
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Instalar Dependencias
```powershell
pip install -r requirements.txt
```

### 4. Ejecutar Migraciones y Poblar Base de Datos
```powershell
python manage.py migrate
python poblar_datos.py
```

### 5. Ejecutar Pruebas Automatizadas
```powershell
python manage.py test catalogo
```

### 6. Levantar Servidor Local
```powershell
python manage.py runserver
```
Acceder en el navegador a: `http://127.0.0.1:8000/` y `http://127.0.0.1:8000/catalogo/`.
