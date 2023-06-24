// Obtener el elemento select
const selectComunas = document.getElementById('comunas');

// Función para crear las opciones del select
function createComunaOption(comuna) {
  const option = document.createElement('option');
  option.value = comuna.id;
  option.textContent = comuna.nombre;
  return option;
}

// Función para cargar las comunas desde la API
function loadComunas() {
  fetch('{% url 'app_geografia:comuna-list' %}')
    .then(response => response.json())
    .then(data => {
      // Limpiar opciones existentes
      selectComunas.innerHTML = '';

      // Crear opción por defecto
      const defaultOption = document.createElement('option');
      defaultOption.value = '';
      defaultOption.textContent = 'Seleccione una comuna';
      selectComunas.appendChild(defaultOption);

      // Crear opciones para cada comuna
      data.forEach(comuna => {
        const option = createComunaOption(comuna);
        selectComunas.appendChild(option);
      });
    })
    .catch(error => {
      console.log('Error:', error);
    });
}

// Cargar las comunas al cargar la página
loadComunas();
