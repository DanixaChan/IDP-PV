// go_despacho.js

const url = 'http://44.205.221.190:8000/despachos/';

async function obtenerDatosDespacho() {
    try {
        const response = await fetch(url);
        const data = await response.json();
        
        if (Array.isArray(data.results)) {
            mostrarDespachos(data.results);
        } else {
            console.error('Los datos recibidos no son un array:', data);
        }
    } catch (error) {
        console.error('Error al obtener los datos:', error);
    }
}

function mostrarDespachos(despachos) {
    const despachoTableBody = document.getElementById('despachoTableBody');

    despachoTableBody.innerHTML = '';

    despachos.forEach(despacho => {
        const row = document.createElement('tr');

        const fechaDespacho = document.createElement('td');
        fechaDespacho.textContent = despacho.fecha_despacho;
        row.appendChild(fechaDespacho);

        const patenteCamion = document.createElement('td');
        patenteCamion.textContent = despacho.patente_camion;
        row.appendChild(patenteCamion);

        const intento = document.createElement('td');
        intento.textContent = despacho.intento;
        row.appendChild(intento);

        const entregado = document.createElement('td');
        entregado.textContent = despacho.entregado ? 'Sí' : 'No';
        row.appendChild(entregado);

        const idCompra = document.createElement('td');
        idCompra.textContent = despacho.id_compra;
        row.appendChild(idCompra);

        const direccionCompra = document.createElement('td');
        direccionCompra.textContent = despacho.direccion_compra;
        row.appendChild(direccionCompra);

        const valorCompra = document.createElement('td');
        valorCompra.textContent = `$${despacho.valor_compra}`;
        row.appendChild(valorCompra);

        despachoTableBody.appendChild(row);
    });
}

