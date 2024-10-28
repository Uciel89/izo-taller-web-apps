import { obtenerProductos, obtenerImagen } from "./api.js";
const listaProductos = document.getElementById("table-lista-productos");

async function mostrarProductos() {
  try {
    const productos = await obtenerProductos();
    listaProductos.innerHTML = "";

    const imagenUrls = await Promise.all(
      productos.map((producto) => obtenerImagen(producto.id_imagen))
    );

    productos.map((producto, index) => {
      const row = document.createElement("tr");
      const imagenUrl = imagenUrls[index];

      row.innerHTML = `
            <td>${producto.codigo}</td>
            <td>${producto.nombre}</td>
            <td>${producto.descripcion}</td>
            <td>${producto.precio}</td>
            <td><img src="${imagenUrl}" alt="Foto de ${producto.nombre}" width="50"></td>
            <td>
                <button class="btn btn-warning btn-sm" onclick="editarProducto('${producto.id}')">Editar</button>
                <button class="btn btn-danger btn-sm" onclick="eliminarProducto('${producto.id}')">Eliminar</button>
            </td>
        `;

        listaProductos.appendChild(row);
    });
  } catch (error) {
    console.error("Error al mostrar productos:", error);
  }
}

document.addEventListener("DOMContentLoaded", mostrarProductos);