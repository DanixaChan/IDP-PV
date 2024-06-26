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

function createCard(despacho) {
    const card = document.createElement('div');
    card.className = 'card mt-2 col-md-3';
    card.style.width = '18rem';

    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    const cardTitle = document.createElement('h5');
    cardTitle.className = 'card-title';
    cardTitle.textContent = `ID Compra: ${despacho.id_compra}`;

    const cardTextFecha = document.createElement('p');
    cardTextFecha.className = 'card-text';
    cardTextFecha.textContent = `Fecha: ${despacho.fecha_despacho}`;

    const cardTextPatente = document.createElement('p');
    cardTextPatente.className = 'card-text';
    cardTextPatente.textContent = `Patente: ${despacho.patente_camion}`;

    const cardTextIntento = document.createElement('p');
    cardTextIntento.className = 'card-text';
    cardTextIntento.textContent = `Intento: ${despacho.intento}`;

    const cardTextEntregado = document.createElement('p');
    cardTextEntregado.className = 'card-text';
    cardTextEntregado.textContent = `Entregado: ${despacho.entregado ? 'Sí' : 'No'}`;

    const cardTextDireccion = document.createElement('p');
    cardTextDireccion.className = 'card-text';
    cardTextDireccion.textContent = `Dirección: ${despacho.direccion_compra}`;

    const cardTextValor = document.createElement('p');
    cardTextValor.className = 'card-text';
    cardTextValor.textContent = `Valor: $${despacho.valor_compra}`;

    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardTextFecha);
    cardBody.appendChild(cardTextPatente);
    cardBody.appendChild(cardTextIntento);
    cardBody.appendChild(cardTextEntregado);
    cardBody.appendChild(cardTextDireccion);
    cardBody.appendChild(cardTextValor);
    card.appendChild(cardBody);

    container.appendChild(card);
}

// Función para mostrar una página específica
function showPage(page) {
    container.innerHTML = '';
    const start = (page - 1) * cardsPerPage;
    const end = start + cardsPerPage;
    
    // Verificar si data.results es una matriz
    if (Array.isArray(data.results)) {
        const pageData = data.results.slice(start, end);
        pageData.forEach(item => createCard(item));
        updatePagination(page);
    } else {
        console.error('Los datos recibidos no tienen el formato esperado:', data);
    }
}

// Función para actualizar los botones de paginación
function updatePagination(page) {
    paginationContainer.innerHTML = '';
    const totalPages = Math.ceil(data.length / cardsPerPage);

    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement('button');
        button.className = 'btn btn-secondary mx-1';
        button.textContent = i;
        if (i === page) {
            button.classList.add('active');
        }
        button.addEventListener('click', () => {
            currentPage = i;
            showPage(i);
        });
        paginationContainer.appendChild(button);
    }
}

// Inicializar la primera página
obtenerDatosDespacho();

function goToPreviousPage() {
    if (currentPage > 1) {
        currentPage--;
        showPage(currentPage);
    }
}

function goToNextPage() {
    const totalPages = Math.ceil(data.length / cardsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        showPage(currentPage);
    }
}

document.getElementById('previousPageBtn').addEventListener('click', goToPreviousPage);
document.getElementById('nextPageBtn').addEventListener('click', goToNextPage);
