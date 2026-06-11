"""Aplicación Flask para el manejador de tareas categorizadas."""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
from models import ManejadorTareas
import json

app = Flask(__name__)
manejador = ManejadorTareas()


@app.route('/')
def index():
    """Ruta principal."""
    return render_template('index.html')


# ===== RUTAS DE CATEGORÍAS =====

@app.route('/api/categorias', methods=['GET'])
def obtener_categorias():
    """Obtiene todas las categorías."""
    categorias = manejador.obtener_todas_categorias()
    return jsonify([cat.to_dict() for cat in categorias])


@app.route('/api/categorias', methods=['POST'])
def crear_categoria():
    """Crea una nueva categoría."""
    datos = request.get_json()
    nombre = datos.get('nombre', '').strip()
    
    if not nombre:
        return jsonify({'error': 'El nombre de la categoría es requerido'}), 400
    
    categoria = manejador.crear_categoria(nombre)
    return jsonify(categoria.to_dict()), 201


@app.route('/api/categorias/<categoria_id>', methods=['PUT'])
def actualizar_categoria(categoria_id):
    """Actualiza una categoría."""
    datos = request.get_json()
    nombre = datos.get('nombre', '').strip()
    
    if not nombre:
        return jsonify({'error': 'El nombre de la categoría es requerido'}), 400
    
    categoria = manejador.actualizar_categoria(categoria_id, nombre)
    if categoria:
        return jsonify(categoria.to_dict())
    return jsonify({'error': 'Categoría no encontrada'}), 404


@app.route('/api/categorias/<categoria_id>', methods=['DELETE'])
def eliminar_categoria(categoria_id):
    """Elimina una categoría."""
    if manejador.eliminar_categoria(categoria_id):
        return jsonify({'mensaje': 'Categoría eliminada'})
    return jsonify({'error': 'Categoría no encontrada'}), 404


# ===== RUTAS DE TAREAS =====

@app.route('/api/tareas', methods=['GET'])
def obtener_tareas():
    """Obtiene todas las tareas."""
    tareas = manejador.obtener_todas_tareas()
    return jsonify([tarea.to_dict() for tarea in tareas])


@app.route('/api/tareas', methods=['POST'])
def crear_tarea():
    """Crea una nueva tarea."""
    datos = request.get_json()
    
    nombre = datos.get('nombre', '').strip()
    descripcion = datos.get('descripcion', '').strip()
    categoria_id = datos.get('categoria_id', '').strip()
    fecha_limite_str = datos.get('fecha_limite', '').strip()
    
    # Validaciones
    if not nombre:
        return jsonify({'error': 'El nombre de la tarea es requerido'}), 400
    if not categoria_id:
        return jsonify({'error': 'La categoría es requerida'}), 400
    if not fecha_limite_str:
        return jsonify({'error': 'La fecha límite es requerida'}), 400
    
    try:
        fecha_limite = datetime.fromisoformat(fecha_limite_str)
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido'}), 400
    
    tarea = manejador.crear_tarea(nombre, descripcion, categoria_id, fecha_limite)
    if tarea:
        return jsonify(tarea.to_dict()), 201
    return jsonify({'error': 'Categoría no encontrada'}), 404


@app.route('/api/tareas/<tarea_id>', methods=['GET'])
def obtener_tarea(tarea_id):
    """Obtiene una tarea específica."""
    tarea = manejador.obtener_tarea(tarea_id)
    if tarea:
        return jsonify(tarea.to_dict())
    return jsonify({'error': 'Tarea no encontrada'}), 404


@app.route('/api/tareas/<tarea_id>', methods=['PUT'])
def actualizar_tarea(tarea_id):
    """Actualiza una tarea."""
    datos = request.get_json()
    
    nombre = datos.get('nombre')
    descripcion = datos.get('descripcion')
    fecha_limite_str = datos.get('fecha_limite')
    
    fecha_limite = None
    if fecha_limite_str:
        try:
            fecha_limite = datetime.fromisoformat(fecha_limite_str)
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido'}), 400
    
    tarea = manejador.actualizar_tarea(tarea_id, nombre, descripcion, fecha_limite)
    if tarea:
        return jsonify(tarea.to_dict())
    return jsonify({'error': 'Tarea no encontrada'}), 404


@app.route('/api/tareas/<tarea_id>/toggle', methods=['PATCH'])
def toggle_tarea(tarea_id):
    """Cambia el estado de una tarea."""
    tarea = manejador.cambiar_estado_tarea(tarea_id)
    if tarea:
        return jsonify(tarea.to_dict())
    return jsonify({'error': 'Tarea no encontrada'}), 404


@app.route('/api/tareas/<tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    """Elimina una tarea."""
    if manejador.eliminar_tarea(tarea_id):
        return jsonify({'mensaje': 'Tarea eliminada'})
    return jsonify({'error': 'Tarea no encontrada'}), 404


@app.route('/api/tareas/categoria/<categoria_id>', methods=['GET'])
def obtener_tareas_por_categoria(categoria_id):
    """Obtiene todas las tareas de una categoría."""
    tareas = manejador.obtener_tareas_por_categoria(categoria_id)
    return jsonify([tarea.to_dict() for tarea in tareas])


@app.route('/api/tareas/pendientes', methods=['GET'])
def obtener_tareas_pendientes():
    """Obtiene todas las tareas pendientes."""
    tareas = manejador.obtener_tareas_pendientes()
    return jsonify([tarea.to_dict() for tarea in tareas])


@app.route('/api/tareas/completadas', methods=['GET'])
def obtener_tareas_completadas():
    """Obtiene todas las tareas completadas."""
    tareas = manejador.obtener_tareas_completadas()
    return jsonify([tarea.to_dict() for tarea in tareas])


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
