"""Script JavaScript para la interfaz web."""

let filtroActual = 'todas';

// ===== INICIALIZACIÓN =====
document.addEventListener('DOMContentLoaded', () => {
    cargarCategorias();
    cargarTareas();
});

// ===== FUNCIONES DE CATEGORÍAS =====

async function cargarCategorias() {
    try {
        const response = await fetch('/api/categorias');
        const categorias = await response.json();
        
        // Actualizar lista de categorías
        const listaCategorias = document.getElementById('lista-categorias');
        listaCategorias.innerHTML = '';
        
        if (categorias.length === 0) {
            listaCategorias.innerHTML = '<div class="item-vacio">No hay categorías. Crea una nueva.</div>';
        } else {
            categorias.forEach(cat => {
                const div = document.createElement('div');
                div.className = 'categoria-item';
                div.innerHTML = `
                    <span class="categoria-nombre">${cat.nombre}</span>
                    <div class="categoria-acciones">
                        <button class="btn btn-edit" onclick="editarCategoria('${cat.id}', '${cat.nombre}')">Editar</button>
                        <button class="btn btn-danger" onclick="eliminarCategoria('${cat.id}')">Eliminar</button>
                    </div>
                `;
                listaCategorias.appendChild(div);
            });
        }
        
        // Actualizar select de categorías en formulario de tareas
        actualizarSelectCategorias(categorias);
    } catch (error) {
        console.error('Error al cargar categorías:', error);
    }
}

function actualizarSelectCategorias(categorias) {
    const select = document.getElementById('input-categoria-tarea');
    const valorActual = select.value;
    
    select.innerHTML = '<option value="">Selecciona una categoría</option>';
    
    categorias.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat.id;
        option.textContent = cat.nombre;
        select.appendChild(option);
    });
    
    select.value = valorActual;
}

function mostrarFormularioCategoria() {
    document.getElementById('formulario-categoria').classList.add('mostrar');
    document.getElementById('input-nombre-categoria').focus();
}

function ocultarFormularioCategoria() {
    document.getElementById('formulario-categoria').classList.remove('mostrar');
    document.getElementById('input-nombre-categoria').value = '';
}

async function crearCategoria() {
    const nombre = document.getElementById('input-nombre-categoria').value.trim();
    
    if (!nombre) {
        alert('Por favor, ingresa un nombre para la categoría');
        return;
    }
    
    try {
        const response = await fetch('/api/categorias', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre })
        });
        
        if (response.ok) {
            ocultarFormularioCategoria();
            cargarCategorias();
        } else {
            alert('Error al crear la categoría');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function editarCategoria(id, nombreActual) {
    const nuevoNombre = prompt('Editar categoría:', nombreActual);
    if (nuevoNombre === null) return;
    
    if (!nuevoNombre.trim()) {
        alert('El nombre no puede estar vacío');
        return;
    }
    
    try {
        const response = await fetch(`/api/categorias/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre: nuevoNombre })
        });
        
        if (response.ok) {
            cargarCategorias();
            cargarTareas();
        } else {
            alert('Error al actualizar la categoría');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function eliminarCategoria(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar esta categoría? También se eliminarán todas sus tareas.')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/categorias/${id}`, { method: 'DELETE' });
        
        if (response.ok) {
            cargarCategorias();
            cargarTareas();
        } else {
            alert('Error al eliminar la categoría');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// ===== FUNCIONES DE TAREAS =====

async function cargarTareas() {
    try {
        let endpoint = '/api/tareas';
        
        if (filtroActual === 'pendientes') {
            endpoint = '/api/tareas/pendientes';
        } else if (filtroActual === 'completadas') {
            endpoint = '/api/tareas/completadas';
        }
        
        const response = await fetch(endpoint);
        const tareas = await response.json();
        
        // Obtener categorías para mapear nombres
        const resCategorias = await fetch('/api/categorias');
        const categorias = await resCategorias.json();
        const mapaCategorias = {};
        categorias.forEach(cat => {
            mapaCategorias[cat.id] = cat.nombre;
        });
        
        const listaTareas = document.getElementById('lista-tareas');
        listaTareas.innerHTML = '';
        
        if (tareas.length === 0) {
            listaTareas.innerHTML = '<div class="item-vacio">No hay tareas en este filtro.</div>';
        } else {
            tareas.forEach(tarea => {
                const fecha = new Date(tarea.fecha_limite);
                const fechaFormato = fecha.toLocaleDateString('es-ES') + ' ' + fecha.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
                
                const div = document.createElement('div');
                div.className = `item ${tarea.completada ? 'tarea-completada' : ''}`;
                div.innerHTML = `
                    <div class="item-header">
                        <div style="display: flex; align-items: center; gap: 10px; flex: 1;">
                            <input type="checkbox" class="checkbox-tarea" ${tarea.completada ? 'checked' : ''} onchange="cambiarEstadoTarea('${tarea.id}')">
                            <div>
                                <div class="item-titulo">${tarea.nombre}</div>
                                ${tarea.descripcion ? `<div class="item-descripcion">${tarea.descripcion}</div>` : ''}
                            </div>
                        </div>
                    </div>
                    <div class="item-meta">
                        <span class="badge badge-categoria">📂 ${mapaCategorias[tarea.categoria_id] || 'Sin categoría'}</span>
                        <span class="badge badge-fecha">📅 ${fechaFormato}</span>
                        ${tarea.completada ? '<span class="badge badge-completada">✓ Completada</span>' : ''}
                    </div>
                    <div class="item-acciones">
                        <button class="btn btn-edit" onclick="mostrarFormularioEditarTarea('${tarea.id}', '${tarea.nombre.replace(/'/g, "\\'").replace(/"/g, '\\"')}', '${tarea.descripcion.replace(/'/g, "\\'").replace(/"/g, '\\"')}')">Editar</button>
                        <button class="btn btn-danger" onclick="eliminarTarea('${tarea.id}')">Eliminar</button>
                    </div>
                `;
                listaTareas.appendChild(div);
            });
        }
    } catch (error) {
        console.error('Error al cargar tareas:', error);
    }
}

function mostrarFormularioTarea() {
    document.getElementById('formulario-tarea').classList.add('mostrar');
    document.getElementById('input-nombre-tarea').focus();
}

function ocultarFormularioTarea() {
    document.getElementById('formulario-tarea').classList.remove('mostrar');
    document.getElementById('input-nombre-tarea').value = '';
    document.getElementById('input-descripcion-tarea').value = '';
    document.getElementById('input-categoria-tarea').value = '';
    document.getElementById('input-fecha-tarea').value = '';
}

async function crearTarea() {
    const nombre = document.getElementById('input-nombre-tarea').value.trim();
    const descripcion = document.getElementById('input-descripcion-tarea').value.trim();
    const categoria_id = document.getElementById('input-categoria-tarea').value;
    const fecha_str = document.getElementById('input-fecha-tarea').value;
    
    if (!nombre) {
        alert('Por favor, ingresa un nombre para la tarea');
        return;
    }
    if (!categoria_id) {
        alert('Por favor, selecciona una categoría');
        return;
    }
    if (!fecha_str) {
        alert('Por favor, selecciona una fecha límite');
        return;
    }
    
    try {
        const fecha_limite = new Date(fecha_str).toISOString();
        
        const response = await fetch('/api/tareas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nombre,
                descripcion,
                categoria_id,
                fecha_limite
            })
        });
        
        if (response.ok) {
            ocultarFormularioTarea();
            cargarTareas();
        } else {
            alert('Error al crear la tarea');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function cambiarEstadoTarea(tareaId) {
    try {
        const response = await fetch(`/api/tareas/${tareaId}/toggle`, {
            method: 'PATCH'
        });
        
        if (response.ok) {
            cargarTareas();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function mostrarFormularioEditarTarea(id, nombre, descripcion) {
    // Por ahora, solo permitimos editar el nombre y descripción vía alert
    const nuevoNombre = prompt('Editar nombre de tarea:', nombre);
    if (nuevoNombre === null) return;
    
    if (!nuevoNombre.trim()) {
        alert('El nombre no puede estar vacío');
        return;
    }
    
    const nuevaDescripcion = prompt('Editar descripción:', descripcion);
    if (nuevaDescripcion === null) return;
    
    editarTarea(id, nuevoNombre, nuevaDescripcion);
}

async function editarTarea(id, nombre, descripcion) {
    try {
        const response = await fetch(`/api/tareas/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nombre: nombre.trim(),
                descripcion: descripcion.trim()
            })
        });
        
        if (response.ok) {
            cargarTareas();
        } else {
            alert('Error al actualizar la tarea');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function eliminarTarea(tareaId) {
    if (!confirm('¿Estás seguro de que deseas eliminar esta tarea?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/tareas/${tareaId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            cargarTareas();
        } else {
            alert('Error al eliminar la tarea');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// ===== FUNCIONES DE FILTRO =====

function filtrarTareas(filtro) {
    filtroActual = filtro;
    
    // Actualizar botones de filtro
    document.querySelectorAll('.filtro-btn').forEach(btn => {
        btn.classList.remove('activo');
    });
    event.target.classList.add('activo');
    
    cargarTareas();
}
