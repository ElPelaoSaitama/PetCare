document.addEventListener('DOMContentLoaded', () => {
  const botonesIncrementar = document.querySelectorAll('.btn-incrementar');
  const botonesDecrementar = document.querySelectorAll('.btn-decrementar');

  botonesIncrementar.forEach((boton) => {
    boton.addEventListener('click', () => {
      const productoId = boton.dataset.productoId;
      const cantidadElement = document.getElementById(`cantidad-${productoId}`);
      let cantidad = parseInt(cantidadElement.textContent);
      cantidad++;
      cantidadElement.textContent = cantidad;

      actualizarCarrito(productoId, cantidad);
    });
  });

  botonesDecrementar.forEach((boton) => {
    boton.addEventListener('click', () => {
      const productoId = boton.dataset.productoId;
      const cantidadElement = document.getElementById(`cantidad-${productoId}`);
      let cantidad = parseInt(cantidadElement.textContent);

      if (cantidad > 1) {
        cantidad--;
        cantidadElement.textContent = cantidad;

        actualizarCarrito(productoId, cantidad);
      }
    });
  });
});

function formatNumber(number) {
  const formattedNumber = number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  return formattedNumber;
}

function actualizarCarrito(productoId, cantidad) {
  const precioUnitario = parseFloat(document.getElementById(`precio-${productoId}`).textContent.slice(2)); // Obtener el precio sin el signo de $
  const subtotal = precioUnitario * cantidad;

  // Actualizar el subtotal del producto
  document.getElementById(`subtotal-${productoId}`).textContent = `$ ${formatNumber(subtotal.toFixed(0))}`;

  // Recalcular el total sumando todos los subtotales de los productos
  let total = 0;
  const subtotales = document.querySelectorAll('[id^="subtotal-"]');
  subtotales.forEach((subtotalElement) => {
    total += parseFloat(subtotalElement.textContent.slice(2).replace('.', ''));
  });

  // Actualizar el total
  document.getElementById('total').textContent = `$ ${formatNumber(total.toFixed(0))}`;
}




