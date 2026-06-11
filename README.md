# Task Manager Categorized

Un manejador de tareas categorizadas con interfaz gráfica web.

## Características

- ✅ Crear, editar y eliminar tareas
- ✅ Organizar tareas por categorías
- ✅ Marcar tareas como completadas
- ✅ Fechas límite para cada tarea
- ✅ Interfaz gráfica web intuitiva
- ✅ Almacenamiento en memoria

## Requisitos

- Python 3.8+
- Flask
- Python-dateutil

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python app.py
```

Luego abre tu navegador en `http://localhost:5000`

## Estructura del Proyecto

```
.
├── app.py                  # Aplicación Flask principal
├── models.py               # Modelos de datos (Tarea, Categoría)
├── requirements.txt        # Dependencias del proyecto
├── static/
│   ├── css/
│   │   └── style.css      # Estilos CSS
│   └── js/
│       └── script.js      # JavaScript del cliente
└── templates/
    └── index.html         # Plantilla HTML principal
```

## Uso

### Crear una Categoría
1. Haz clic en "+ Nueva Categoría"
2. Ingresa el nombre de la categoría
3. Haz clic en "Crear"

### Crear una Tarea
1. Haz clic en "+ Nueva Tarea"
2. Completa:
   - Nombre de la tarea
   - Descripción (opcional)
   - Categoría
   - Fecha límite
3. Haz clic en "Crear"

### Gestionar Tareas
- **Completar**: Marca el checkbox de la tarea
- **Editar**: Haz clic en "Editar" para cambiar nombre o descripción
- **Eliminar**: Haz clic en "Eliminar"

### Filtrar Tareas
- **Todas**: Muestra todas las tareas
- **Pendientes**: Muestra solo tareas sin completar
- **Completadas**: Muestra solo tareas completadas

## API REST

### Categorías
- `GET /api/categorias` - Obtener todas las categorías
- `POST /api/categorias` - Crear nueva categoría
- `PUT /api/categorias/<id>` - Actualizar categoría
- `DELETE /api/categorias/<id>` - Eliminar categoría

### Tareas
- `GET /api/tareas` - Obtener todas las tareas
- `POST /api/tareas` - Crear nueva tarea
- `GET /api/tareas/<id>` - Obtener tarea específica
- `PUT /api/tareas/<id>` - Actualizar tarea
- `PATCH /api/tareas/<id>/toggle` - Cambiar estado de tarea
- `DELETE /api/tareas/<id>` - Eliminar tarea
- `GET /api/tareas/categoria/<categoria_id>` - Obtener tareas de una categoría
- `GET /api/tareas/pendientes` - Obtener tareas pendientes
- `GET /api/tareas/completadas` - Obtener tareas completadas

## Ejemplo de Datos

### Formato de Categoría
```json
{
  "id": "uuid-aqui",
  "nombre": "Trabajo"
}
```

### Formato de Tarea
```json
{
  "id": "uuid-aqui",
  "nombre": "Completar proyecto",
  "descripcion": "Finalizar el módulo de autenticación",
  "categoria_id": "uuid-categoria",
  "completada": false,
  "fecha_limite": "2026-06-20T18:00:00",
  "creada_en": "2026-06-11T10:30:00"
}
```
