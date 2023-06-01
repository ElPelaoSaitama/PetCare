$(document).ready(function() {
    $('.diagnostico-button').on('click', function() {
      var agendamientoId = $(this).data('agendamiento-id');
      $('#modal-diagnostico-' + agendamientoId).show();
    });
  
    $('.diagnostico-form').on('submit', function(e) {
      e.preventDefault();
      var form = $(this);
      var agendamientoId = form.find('input[name="agendamiento_id"]').val();
      var diagnostico = form.find('textarea[name="diagnostico"]').val();
  
      $.ajax({
        type: 'POST',
        url: '/guardar-diagnostico/',
        data: {
          agendamiento_id: agendamientoId,
          diagnostico: diagnostico,
          csrfmiddlewaretoken: '{{ csrf_token }}',
        },
        success: function(response) {
          window.location.reload();
        },
        error: function(error) {
          console.log(error);
        }
      });
    });
  });
  