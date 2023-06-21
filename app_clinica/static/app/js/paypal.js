// Configurar el botón de PayPal
paypal.Buttons({
    createOrder: function (data, actions) {
      return actions.order.create({
        purchase_units: [{
          amount: {
            value: '{{ total }}', // Inserta aquí el valor total del carrito desde tu contexto
            currency_code: 'USD'
          }
        }]
      });
    },
    onApprove: function (data, actions) {
      return actions.order.capture().then(function (details) {
        // Vaciar el carrito
        vaciarCarrito();
  
        // Mostrar mensaje de pago exitoso utilizando SweetAlert
        Swal.fire({
          icon: 'success',
          title: '¡Pago exitoso!',
          text: 'La transacción se ha completado correctamente.',
          confirmButtonText: 'Aceptar',
          onAfterClose: function () {
            window.location.reload(true);
          }
        });
      });
    }
  }).render('#paypal-button-container');
  
  function vaciarCarrito() {
    // Realiza la petición AJAX al servidor para vaciar el carrito
    // Puedes utilizar la función fetch() para hacer la petición al servidor y enviar los datos
  
    fetch('{% url 'app_tienda:vaciar_carrito' %}', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // Aquí puedes manejar la respuesta del servidor si es necesario
        console.log(data);
      })
      .catch(function (error) {
        console.error('Error:', error);
      });
  }
  
  function getCookie(name) {
    var cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
  }
  