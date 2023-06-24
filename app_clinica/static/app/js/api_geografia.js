$(document).ready(function() {
  const regionesUrl = 'http://petcare.ddns.net/api-geografia/api/regiones/';

  // Obtener regiones mediante AJAX
  $.ajax({
    url: regionesUrl,
    method: 'GET',
    dataType: 'json',
    success: function(data) {
      const $regionSelect = $('#region');
      $regionSelect.empty(); // Limpiar opciones existentes

      // Agregar opción de placeholder
      const placeholderOption = $('<option>').val('').text('Seleccione región');
      $regionSelect.append(placeholderOption);

      // Agregar opciones de regiones al select
      data.forEach(function(region) {
        const option = $('<option>').val(region.id).text(region.nombre);
        $regionSelect.append(option);
      });
    },
    error: function(xhr, textStatus, errorThrown) {
      console.log('Error al obtener regiones:', errorThrown);
    }
  });
});

// Obtener referencias a los elementos <select>
var $regionSelect = $('#region');
var $comunasSelect = $('#comunas');

// Función para cargar las comunas basadas en la región seleccionada
function cargarComunas() {
  var regionId = $regionSelect.val();

  // Verificar si se ha seleccionado una región
  if (regionId) {
    // Realizar una solicitud AJAX a la API para obtener las comunas de la región seleccionada
    // Aquí debes reemplazar la URL con la ruta correcta a tu vista de API de comunas
    var url = '/api-geografia/api/comunas/?region_id=' + regionId;
    $.ajax({
      url: url,
      method: 'GET',
      dataType: 'json',
      success: function(data) {
        // Limpiar el <select> de comunas
        $comunasSelect.empty();

        // Agregar opción de placeholder
        const placeholderOption = $('<option>').val('').text('Seleccione comuna');
        $comunasSelect.append(placeholderOption);

        // Agregar las opciones de comunas al <select>
        data.forEach(function(comuna) {
          var option = $('<option>').val(comuna.id).text(comuna.nombre);
          $comunasSelect.append(option);
        });
      },
      error: function(xhr, textStatus, errorThrown) {
        console.log('Error al cargar las comunas:', errorThrown);
      }
    });
  } else {
    // Si no se ha seleccionado una región, limpiar el <select> de comunas
    $comunasSelect.empty();
  }
}

// Asociar el evento "change" al <select> de regiones
$regionSelect.on('change', cargarComunas);

// Cargar las regiones al cargar la página
cargarComunas();
