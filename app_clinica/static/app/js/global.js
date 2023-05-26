
    document.addEventListener('DOMContentLoaded', function() {
        var rutInput = document.getElementById('rut');
        rutInput.addEventListener('input', function() {
            var value = rutInput.value;
            value = value.replace(/[^\dkK]+/g, ''); // Eliminar caracteres no válidos
            var formattedValue = '';
            for (var i = 0; i < value.length; i++) {
                if (i === 2 || i === 5) {
                    formattedValue += '.'; // Agregar punto después del tercer y sexto dígito
                } else if (i === value.length - 1) {
                    formattedValue += '-' + value.charAt(i); // Agregar guion y dígito verificador al final
                } else {
                    formattedValue += value.charAt(i);
                }
            }
            rutInput.value = formattedValue;
        });
    });
