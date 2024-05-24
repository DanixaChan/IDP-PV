// go_despacho.js
const container = document.getElementById('div-grid-ord');
const paginationContainer = document.getElementById('pagination');
const cardsPerPage = 9;
let currentPage = 1;
let data = [];

const url = '/obtener_datos_ec2';

async function obtenerDatosDespacho() {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Error al obtener los datos');
        }
        const result = await response.json();
        console.log(result); // Agregar esta línea para ver los datos recibidos
        data = result;
        showPage(currentPage);
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

