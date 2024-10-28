// IMPORTACIÓN DE MODULOS QUE PROVIENEN DEL ARCHIVO api.js
import {
  crearProductoRequest,
  eliminarProductoRequest,
  modificarProductoRequest,
  obtenerProductosRequest,
} from "./api";

// LLAMADA A ELEMENTOS ESPECIFICOS
document.getElementById("btn-crear-producto").addEventListener("click", function () {
  abrirModal();
});

document.getElementById("formCrearProducto").addEventListener("submit", function (event) {
  event.preventDefault();
  crearProducto();
});

document.getElementById("formEditarProducto").addEventListener("submit", function (event) {
  event.preventDefault();
  actualizarProducto();
});

// MÉTODO PARA MOSTRAR TODOS LOS PRODUCTOS
async function mostrarProductos() {
  try {
    const listaProductos = document.getElementById("table-lista-productos");
    const response = await obtenerProductosRequest();

    if(Object.keys(response).length === 0) {
      listaProductos.innerHTML = "";
      const row = document.createElement("tr");
      row.innerHTML = `<td colspan="6" class="text-center">No hay datos</td>`
      listaProductos.appendChild(row);
    } else {
      const productos = response.lista_productos;
      listaProductos.innerHTML = "";

      productos.map((producto, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
              <td>${producto.codigo}</td>
              <td>${producto.nombre}</td>
              <td style="text-overflow: ellipsis;">${producto.descripcion}</td>
              <td>${producto.precio}</td>
              <td><img src="http://localhost:8000/v1/productos/imagen/${producto.codigo}" alt="Foto de ${producto.nombre}" width="50"></td>
              <td>
                  <button class="btn btn-warning btn-sm btn-editar-producto">Editar</button>
                  <button class="btn btn-danger btn-sm btn-eliminar-producto">Eliminar</button>
              </td>
          `;

        row.querySelector(".btn-editar-producto").onclick = () => abrirModalEditar(producto);
        row.querySelector(".btn-eliminar-producto").onclick = () => abrirModalEliminar(producto.codigo);
        listaProductos.appendChild(row);
    });
    }
  } catch (error) {
    console.error("Error al mostrar productos:", error);
  }
}

// MÉTODOS PARA ABIRIR LOS DIREFENTES MODALS
function abrirModal() {
  document.getElementById("floatingInputEditarCodigo").value = "";
  document.getElementById("floatingInputEditarNombre").value = "";
  document.getElementById("floatingInputEditarDescripcion").value = "";
  document.getElementById("floatingInputEditartPrecio").value = "";
  document.getElementById("formImage").value = "";
  var modal = new bootstrap.Modal(
    document.getElementById("modalCrearProducto")
  );
  modal.show();
}

function abrirModalEditar(producto) {
  const modal = new bootstrap.Modal(
    document.getElementById("modalEditarProducto")
  );

  document.getElementById("floatingInputEditarCodigo").value = producto.codigo;
  document.getElementById("floatingInputEditarNombre").value = producto.nombre;
  document.getElementById("floatingInputEditarDescripcion").value =
    producto.descripcion;
  document.getElementById("floatingInputEditartPrecio").value = producto.precio;

  modal.show();
}

function abrirModalEliminar(codigo) {
  const modalEliminar = new bootstrap.Modal(document.getElementById("modalEliminarProducto"));
  modalEliminar.show();
  eliminarProducto(codigo);
}

// MÉTODOS PARA EJECUTAR LAS LLAMADAS A LA API
function crearProducto() {
  const modalCrear = bootstrap.Modal.getInstance(
    document.getElementById("modalCrearProducto")
  );

  const codigo = document.getElementById("floatingInputCodigo").value;
  const nombre = document.getElementById("floatingInputNombre").value;
  const descripcion = document.getElementById("floatingDescripcion").value;
  const precio = document.getElementById("floatingInputPrecio").value;
  const imagen = document.getElementById("formImage").files[0];

  try {
    crearProductoRequest(codigo, nombre, precio, descripcion, imagen);
    modalCrear.hide();
    mostrarProductos();
  } catch (error) {
    console.error(error);
  }
}

function actualizarProducto() {
  const modalEdit = bootstrap.Modal.getInstance(
    document.getElementById("modalEditarProducto")
  );

  const codigo = document.getElementById("floatingInputEditarCodigo").value;
  const nombre = document.getElementById("floatingInputEditarNombre").value;
  const descripcion = document.getElementById(
    "floatingInputEditarDescripcion"
  ).value;
  const precio = document.getElementById("floatingInputEditartPrecio").value;
  const imagen = document.getElementById("formEditarImage").files[0];

  try {
    modificarProductoRequest(codigo, nombre, precio, descripcion, imagen);
    modalEdit.hide();
    mostrarProductos();
  } catch (error) {
    console.error(error);
  }
}

function eliminarProducto(codigo) {
  const modalEliminar = bootstrap.Modal.getInstance(document.getElementById("modalEliminarProducto"));

  try {
    document.getElementById("btnConfirmarEliminar").addEventListener("click", () => {
        eliminarProductoRequest(codigo)
          .then(() => {
            modalEliminar.hide();
            mostrarProductos();
          });
      });
  } catch (error) {
    console.error(error);
  }
}

mostrarProductos();
