export async function obtenerProductos() {
    try {
        const response = await fetch('http://127.0.0.1:8000/v1/productos');
        if (!response.ok) {
            if (response.data.status === 404) {
                console.error("Ruta no encontrada: productos no disponibles.");
                return []; 
            }
            throw new Error('Error al obtener los productos');
        }
        const productos = await response.json();
        return productos;
    } catch (error) {
        console.error(error);
    }
}

export async function crearProducto(nombre, precio, descripcion) {
    try {
        const response = await fetch('http://127.0.0.1:8000/v1/productos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre: nombre,
                precio: precio,
                descripcion: descripcion
            })
        });
        if (!response.ok) {
            throw new Error('Error al crear el producto');
        }
        const producto = await response.json();
        console.log('Producto creado:', producto);
        return producto;
    } catch (error) {
        console.error(error);
    }
}

export async function obtenerImagen(idImagen) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/v1/productos/imagen/${idImagen}`);
        if (!response.ok) {
            throw new Error('Error al obtener la imagen');
        }
        const imagenBlob = await response.blob();
        const imagenUrl = URL.createObjectURL(imagenBlob);
        console.log('URL de la imagen:', imagenUrl);
        return imagenUrl;
    } catch (error) {
        console.error(error);
        return ""
    }
}

export async function modificarProducto(productoId, nombre, precio, descripcion) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/v1/productos/${productoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre: nombre,
                precio: precio,
                descripcion: descripcion
            })
        });
        if (!response.ok) {
            throw new Error('Error al modificar el producto');
        }
        const productoActualizado = await response.json();
        console.log('Producto actualizado:', productoActualizado);
        return productoActualizado;
    } catch (error) {
        console.error(error);
    }
}

export async function eliminarProducto(productoId) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/v1/productos/${productoId}`, {
            method: 'DELETE'
        });
        if (!response.ok) {
            throw new Error('Error al eliminar el producto');
        }
        console.log('Producto eliminado');
        return true;
    } catch (error) {
        console.error(error);
        return false;
    }
}
