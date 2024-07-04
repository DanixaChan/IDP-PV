// devolucion.js

$(document).ready(function() {
    $('#btn-confirmar').click(function() {
        var items_boleta = $(this).data('items-boleta');

        $.ajax({
            url: '/procesar_devolucion',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ items_boleta: items_boleta }),  // Asegúrate de enviar los datos correctamente
            success: function(response) {
                alert(response.message);
                window.location.href = '/b_boleta'; // Redirige a la página de boletas después de la confirmación
            },
            error: function(xhr) {
                alert('Error: ' + xhr.responseJSON.message);
            }
        });
    });
});
