$(document).ready(function() {
    $('.rut-input').on('input', function() {
      let rutValue = $(this).val();
      rutValue = rutValue.replace(/[^\dkK]+/g, ''); // Eliminar caracteres no numéricos ni "k" (u "K")
      rutValue = rutValue.replace(/^(\d{2})(\d{3})(\d{3})([\dkK]{1})$/, '$1.$2.$3-$4'); // Formato XX.XXX.XXX-X o XX.XXX.XXX-K
      $(this).val(rutValue);
    });
  });
  