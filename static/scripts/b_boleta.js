// b_boleta.js

const container = document.getElementById('div-grid-bol');
const paginationContainer = document.getElementById('pagination');
const cardsPerPage = 12;
let currentPage = 1;
let data = []; // Inicializa data como un arreglo vacío para almacenar los datos recibidos

const url = '/obtener_datos_ec2_boletas';

async function obtenerDatosBoletas() {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Error al obtener los datos');
        }
        const result = await response.json();
        console.log(result); // Para verificar los datos recibidos en la consola del navegador
        data = result;
        showPage(currentPage);
    } catch (error) {
        console.error('Error al obtener los datos:', error);
    }
}

function createCard(boleta) {
    const card = document.createElement('div');
    card.className = 'card mt-5';
    card.style.width = '18rem';
    card.style.height = '18rem';

    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    const cardTitle = document.createElement('h5');
    cardTitle.className = 'card-title';
    cardTitle.textContent = `Id: ${boleta.id}`;

    const cardTextFecha = document.createElement('p');
    cardTextFecha.className = 'card-text';
    cardTextFecha.textContent = `Fecha: ${boleta.fecha_emision}`;

    const cardTextNombre = document.createElement('p');
    cardTextNombre.className = 'card-text';
    cardTextNombre.textContent = `Cliente: ${boleta.cliente}`;

    const cardTextTotal = document.createElement('p');
    cardTextTotal.className = 'card-text';
    cardTextTotal.textContent = `Total: ${boleta.total}`;

    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardTextFecha);
    cardBody.appendChild(cardTextNombre);
    cardBody.appendChild(cardTextTotal);
    card.appendChild(cardBody);

    container.appendChild(card);
}

function showPage(page) {
    container.innerHTML = '';
    const start = (page - 1) * cardsPerPage;
    const end = start + cardsPerPage;
    const pageData = data.slice(start, end);

    pageData.forEach(item => createCard(item));
    updatePagination(page);
}

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
        button.addEventListener('click', () => showPage(i));
        paginationContainer.appendChild(button);
    }
}

obtenerDatosBoletas();
