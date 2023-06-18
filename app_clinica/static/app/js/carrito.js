function sumarCantidad(productoId) {
    var cantidadElement = document.getElementById('cantidad-' + productoId);
    var subtotalElement = document.getElementById('subtotal-' + productoId);
    var precioElement = document.getElementById('precio-' + productoId);
    var totalElement = document.getElementById('total');
  
    var cantidad = parseInt(cantidadElement.innerHTML);
    var precio = parseFloat(precioElement.innerHTML.slice(1).replace(/\./g, '').replace(',', '.'));
    var subtotal = parseFloat(subtotalElement.innerHTML.slice(1).replace(/\./g, '').replace(',', '.'));
    var total = parseFloat(totalElement.innerHTML.slice(1).replace(/\./g, '').replace(',', '.'));
  
    cantidad++;
    subtotal += precio;
    total += precio;
  
    cantidadElement.innerHTML = cantidad;
    subtotalElement.innerHTML = '$' + subtotal.toLocaleString('es-CL');
    totalElement.innerHTML = '$' + total.toLocaleString('es-CL');
  }
  
  function restarCantidad(productoId) {
    var cantidadElement = document.getElementById('cantidad-' + productoId);
    var subtotalElement = document.getElementById('subtotal-' + productoId);
    var precioElement = document.getElementById('precio-' + productoId);
    var totalElement = document.getElementById('total');
  
    var cantidad = parseInt(cantidadElement.innerHTML);
    var precio = parseFloat(precioElement.innerHTML.slice(1).replace(/\./g, '').replace(',', '.'));
    var subtotal = parseFloat(subtotalElement.innerHTML.slice(1).replace(/\./g, '').replace(',', '.'));
    var total = parseFloat(totalElement.innerHTML.slice(1).replace(/\./g, '').replace(',', '.'));
  
    if (cantidad > 1) {
      cantidad--;
      subtotal -= precio;
      total -= precio;
  
      cantidadElement.innerHTML = cantidad;
      subtotalElement.innerHTML = '$' + subtotal.toLocaleString('es-CL');
      totalElement.innerHTML = '$' + total.toLocaleString('es-CL');
    }
  }
  
  function vaciarCarrito() {
    if (confirm('¿Estás seguro de que deseas vaciar el carrito?')) {
      fetch('/petstore/vaciar_carrito/')
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            window.location.reload();
          }
        })
        .catch(error => {
          console.error('Error al vaciar el carrito:', error);
        });
    }
  }