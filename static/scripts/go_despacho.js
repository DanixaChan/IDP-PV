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
    const despachoContainer = document.querySelector('.despacho-container');
    despachoContainer.innerHTML = '';

    despachos.forEach(despacho => {
        const despachoElement = document.createElement('div');
        despachoElement.classList.add('despacho-item');

        const fechaDespacho = document.createElement('p');
        fechaDespacho.textContent = `Fecha de despacho: ${despacho.fecha_despacho}`;

        const patenteCamion = document.createElement('p');
        patenteCamion.textContent = `Patente del camión: ${despacho.patente_camion}`;

        const intento = document.createElement('p');
        intento.textContent = `Intento: ${despacho.intento}`;

        const entregado = document.createElement('p');
        entregado.textContent = `Entregado: ${despacho.entregado ? 'Sí' : 'No'}`;

        const idCompra = document.createElement('p');
        idCompra.textContent = `ID de compra: ${despacho.id_compra}`;

        const direccionCompra = document.createElement('p');
        direccionCompra.textContent = `Dirección de compra: ${despacho.direccion_compra}`;

        const valorCompra = document.createElement('p');
        valorCompra.textContent = `Valor de compra: $${despacho.valor_compra}`;

        despachoElement.appendChild(fechaDespacho);
        despachoElement.appendChild(patenteCamion);
        despachoElement.appendChild(intento);
        despachoElement.appendChild(entregado);
        despachoElement.appendChild(idCompra);
        despachoElement.appendChild(direccionCompra);
        despachoElement.appendChild(valorCompra);

        despachoContainer.appendChild(despachoElement);
    });
}

obtenerDatosDespacho();
