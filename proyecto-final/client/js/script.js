// Importamos modulos
import { createProduct, updateProduct, deleteProduct } from './api.js'

// Instacias de los modals
const modalCreateElement = document.getElementById('modalCreateProduct');
const modalUpdateElement = document.getElementById('modalUpdateProduct');
const modalDeleteElement = document.getElementById('modalDeleteProduct');

const modalCreateProduct = new bootstrap.Modal(modalCreateElement);
const modalUpdateProduct = new bootstrap.Modal(modalUpdateElement);
const modalDeleteProduct = new bootstrap.Modal(modalDeleteElement);

function openCreateModal() {
  // Limpiamos los inputs por si llegue a existir algún dato
  document.getElementById("floatingInputCodigo").value = "";
  document.getElementById("floatingInputNombre").value = "";
  document.getElementById("floatingDescripcion").value = "";
  document.getElementById("floatingInputPrecio").value = "";

  modalCreateProduct.show()
}

function openUpdateModal(item) {
    let row = item.closest("tr");

    let codigoProducto = row.cells[0].innerText;
    let nombreProducto = row.cells[1].innerText;
    let descripcionProducto = row.cells[2].innerText;
    let precioProducto = row.cells[3].innerText;

    document.getElementById("floatingInputCodigo").value = codigoProducto;
    document.getElementById("floatingInputNombre").value = nombreProducto;
    document.getElementById("floatingDescripcion").value = descripcionProducto;
    document.getElementById("floatingInputPrecio").value = precioProducto;  

    modalUpdateProduct.show();
}

function openDeleteModal(item) {
  modalDeleteProduct.show();

  // Obtenemos la fila de la tabla
  let row = item.closest("tr");
  
  // Instaciamos el botón para eliminar el registro
  const deleteButton = document.getElementById("deleteButton");
  deleteButton.addEventListener("click", function () {
    
    // Ejecutamos la función deleteProducto para borrar el producto del sistema
    deleteProduct(row.cells[0].innerText, modalDeleteProduct)    
  });
}

// Escuchamos el evento submit tanto del formulario para crear como actualizar y ejecutamos las funciones correspondientes
document.getElementById('formCreateProduct').addEventListener('submit', function(event) {
    // Prevenir la recarga de la página al enviar el formulario
    event.preventDefault(); 

    // Crear un objeto FormData para manejar los datos del formulario y el archivo
    let formData = new FormData();

    // Agregar los datos del formulario al FormData
    formData.append('codigo', document.getElementById('floatingInputCodigo').value);
    formData.append('nombre', document.getElementById('floatingInputNombre').value);
    formData.append('descripcion', document.getElementById('floatingDescripcion').value);
    formData.append('precio', parseFloat(document.getElementById('floatingInputPrecio').value));

    // Agregar el archivo de imagen al FormData
    let imageFile = document.getElementById('formImage').files[0];
    if (imageFile) {
        formData.append('foto', imageFile);
    }
    
    // Llamar a la función createProduct para hacer el POST
    createProduct(product);
});

document.getElementById('formUpdateProduct').addEventListener('submit', function(event) {
  // Prevenir la recarga de la página al enviar el formulario
  event.preventDefault(); 

  // Crear un objeto FormData para manejar los datos del formulario y el archivo
  let formData = new FormData();

  // Agregar los datos del formulario al FormData
  formData.append('codigo', document.getElementById('floatingInputCodigo').value);
  formData.append('nombre', document.getElementById('floatingInputNombre').value);
  formData.append('descripcion', document.getElementById('floatingDescripcion').value);
  formData.append('precio', parseFloat(document.getElementById('floatingInputPrecio').value));

  // Agregar el archivo de imagen al FormData
  let imageFile = document.getElementById('formImage').files[0];
  if (imageFile) {
      formData.append('foto', imageFile);
  }
  
  // Llamar a la función createProduct para hacer el POST
  updateProduct(product);
});