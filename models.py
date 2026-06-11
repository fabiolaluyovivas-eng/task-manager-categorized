"""Modelos de datos para el manejador de tareas."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import uuid


@dataclass
class Categoria:
    """Modelo de una categoría."""
    nombre: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        """Convierte la categoría a diccionario."""
        return {
            'id': self.id,
            'nombre': self.nombre
        }


@dataclass
class Tarea:
    """Modelo de una tarea."""
    nombre: str
    descripcion: str
    categoria_id: str
    fecha_limite: datetime
    completada: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    creada_en: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """Convierte la tarea a diccionario."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'categoria_id': self.categoria_id,
            'completada': self.completada,
            'fecha_limite': self.fecha_limite.isoformat(),
            'creada_en': self.creada_en.isoformat()
        }

    def cambiar_estado(self):
        """Alterna el estado de la tarea."""
        self.completada = not self.completada


class ManejadorTareas:
    """Manejador principal de tareas y categorías."""

    def __init__(self):
        """Inicializa el manejador."""
        self.tareas: dict[str, Tarea] = {}
        self.categorias: dict[str, Categoria] = {}

    # ===== MÉTODOS DE CATEGORÍAS =====

    def crear_categoria(self, nombre: str) -> Categoria:
        """Crea una nueva categoría.
        
        Args:
            nombre: Nombre de la categoría
            
        Returns:
            La categoría creada
        """
        categoria = Categoria(nombre=nombre)
        self.categorias[categoria.id] = categoria
        return categoria

    def obtener_categoria(self, categoria_id: str) -> Categoria | None:
        """Obtiene una categoría por ID.
        
        Args:
            categoria_id: ID de la categoría
            
        Returns:
            La categoría o None si no existe
        """
        return self.categorias.get(categoria_id)

    def obtener_todas_categorias(self) -> List[Categoria]:
        """Obtiene todas las categorías.
        
        Returns:
            Lista de todas las categorías
        """
        return list(self.categorias.values())

    def actualizar_categoria(self, categoria_id: str, nombre: str) -> Categoria | None:
        """Actualiza el nombre de una categoría.
        
        Args:
            categoria_id: ID de la categoría
            nombre: Nuevo nombre
            
        Returns:
            La categoría actualizada o None si no existe
        """
        categoria = self.categorias.get(categoria_id)
        if categoria:
            categoria.nombre = nombre
        return categoria

    def eliminar_categoria(self, categoria_id: str) -> bool:
        """Elimina una categoría y sus tareas asociadas.
        
        Args:
            categoria_id: ID de la categoría
            
        Returns:
            True si se eliminó, False si no existía
        """
        if categoria_id in self.categorias:
            # Eliminar tareas asociadas
            tareas_a_eliminar = [
                tarea_id for tarea_id, tarea in self.tareas.items()
                if tarea.categoria_id == categoria_id
            ]
            for tarea_id in tareas_a_eliminar:
                del self.tareas[tarea_id]
            
            del self.categorias[categoria_id]
            return True
        return False

    # ===== MÉTODOS DE TAREAS =====

    def crear_tarea(self, nombre: str, descripcion: str, 
                    categoria_id: str, fecha_limite: datetime) -> Tarea | None:
        """Crea una nueva tarea.
        
        Args:
            nombre: Nombre de la tarea
            descripcion: Descripción de la tarea
            categoria_id: ID de la categoría
            fecha_limite: Fecha límite de la tarea
            
        Returns:
            La tarea creada o None si la categoría no existe
        """
        if categoria_id not in self.categorias:
            return None
        
        tarea = Tarea(
            nombre=nombre,
            descripcion=descripcion,
            categoria_id=categoria_id,
            fecha_limite=fecha_limite
        )
        self.tareas[tarea.id] = tarea
        return tarea

    def obtener_tarea(self, tarea_id: str) -> Tarea | None:
        """Obtiene una tarea por ID.
        
        Args:
            tarea_id: ID de la tarea
            
        Returns:
            La tarea o None si no existe
        """
        return self.tareas.get(tarea_id)

    def obtener_todas_tareas(self) -> List[Tarea]:
        """Obtiene todas las tareas.
        
        Returns:
            Lista de todas las tareas
        """
        return list(self.tareas.values())

    def obtener_tareas_por_categoria(self, categoria_id: str) -> List[Tarea]:
        """Obtiene todas las tareas de una categoría.
        
        Args:
            categoria_id: ID de la categoría
            
        Returns:
            Lista de tareas de la categoría
        """
        return [
            tarea for tarea in self.tareas.values()
            if tarea.categoria_id == categoria_id
        ]

    def actualizar_tarea(self, tarea_id: str, nombre: str = None,
                        descripcion: str = None, 
                        fecha_limite: datetime = None) -> Tarea | None:
        """Actualiza una tarea.
        
        Args:
            tarea_id: ID de la tarea
            nombre: Nuevo nombre (opcional)
            descripcion: Nueva descripción (opcional)
            fecha_limite: Nueva fecha límite (opcional)
            
        Returns:
            La tarea actualizada o None si no existe
        """
        tarea = self.tareas.get(tarea_id)
        if tarea:
            if nombre is not None:
                tarea.nombre = nombre
            if descripcion is not None:
                tarea.descripcion = descripcion
            if fecha_limite is not None:
                tarea.fecha_limite = fecha_limite
        return tarea

    def cambiar_estado_tarea(self, tarea_id: str) -> Tarea | None:
        """Cambia el estado de una tarea.
        
        Args:
            tarea_id: ID de la tarea
            
        Returns:
            La tarea con estado actualizado o None si no existe
        """
        tarea = self.tareas.get(tarea_id)
        if tarea:
            tarea.cambiar_estado()
        return tarea

    def eliminar_tarea(self, tarea_id: str) -> bool:
        """Elimina una tarea.
        
        Args:
            tarea_id: ID de la tarea
            
        Returns:
            True si se eliminó, False si no existía
        """
        if tarea_id in self.tareas:
            del self.tareas[tarea_id]
            return True
        return False

    def obtener_tareas_pendientes(self) -> List[Tarea]:
        """Obtiene todas las tareas sin hacer.
        
        Returns:
            Lista de tareas pendientes
        """
        return [tarea for tarea in self.tareas.values() if not tarea.completada]

    def obtener_tareas_completadas(self) -> List[Tarea]:
        """Obtiene todas las tareas completadas.
        
        Returns:
            Lista de tareas completadas
        """
        return [tarea for tarea in self.tareas.values() if tarea.completada]
