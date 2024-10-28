// MÉTODO PARA OBTENER TODOS LOS PRODUCTOS
export async function obtenerProductosRequest() {
  try {
    const response = await fetch("http://127.0.0.1:8000/v1/productos", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const productos = await response.json();
    return productos;
  } catch (error) {
    console.error(error);
  }
}

// MÉTODO PARA CREAR UN PRODUCTO
export async function crearProductoRequest(
  codigo,
  nombre,
  precio,
  descripcion,
  foto = null
) {
  try {
    const formData = new FormData();

    if (codigo) formData.append("codigo", parseInt(codigo));
    if (nombre) formData.append("nombre", nombre);
    
    if (precio !== undefined) formData.append("precio", parseInt(precio));
    if (descripcion) formData.append("descripcion", descripcion);
    if (foto) formData.append("foto", foto);

    const response = await fetch("http://127.0.0.1:8000/v1/productos", {
      method: "POST",
      body: formData,
    });
    const producto = await response.json();
    return producto;
  } catch (error) {
    console.error(error);
  }
}

// MÉTODO PARA ACTUALIZAR UN PRODUCTO
export async function modificarProductoRequest(
  codigo,
  nombre,
  precio,
  descripcion,
  foto = null
) {
  try {
    const formData = new FormData();
    if (nombre) formData.append("nombre", nombre);
    if (precio !== undefined) formData.append("precio", precio);
    if (descripcion) formData.append("descripcion", descripcion);
    if (foto) formData.append("foto", foto); 

    const response = await fetch(
      `http://127.0.0.1:8000/v1/productos/${codigo}`,
      {
        method: "PUT",
        body: formData,
      }
    );

    if (!response.ok) {
      throw new Error("Error al modificar el producto");
    }

    const productoActualizado = await response.json();
    return productoActualizado;
  } catch (error) {
    console.error("Error en modificarProducto:", error);
    return null;
  }
}

// MÉTODO PARA ELIMINAR UN PRODUCTO
export async function eliminarProductoRequest(productoId) {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/v1/productos/${productoId}`,
      {
        method: "DELETE",
      }
    );
    return true;
  } catch (error) {
    console.error(error);
    return false;
  }
}
