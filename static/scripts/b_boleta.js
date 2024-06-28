// b_boleta.js

const input = document.querySelector(".form-control");
const calendar = document.getElementById("calend-compra");
const form = document.getElementById("form-filt");

const container = document.getElementById('div-grid-bol');
const paginationContainer = document.getElementById('pagination');
const cardsPerPage = 12;
let currentPage = 1;

// Datos de ejemplo
let data = [
    // { id: 1, nombre_comprador: "Juan Pérez", rut_comprador: "12345678-9", fecha: '2024-05-18' },
    // { id: 2, nombre_comprador: "Ana Gómez", rut_comprador: "98765432-1", fecha: '2024-05-18' },
    // { id: 3, nombre_comprador: "Luis Martínez", rut_comprador: "12345987-0", fecha: '2024-05-18' },
    // { id: 4, nombre_comprador: "Carlos Díaz", rut_comprador: "23456789-1", fecha: '2024-05-18' },
    // { id: 5, nombre_comprador: "María López", rut_comprador: "34567890-2", fecha: '2024-05-18' },
    // { id: 6, nombre_comprador: "Pedro García", rut_comprador: "45678901-3", fecha: '2024-05-18' },
    // Agrega más datos según sea necesario
];

const url = '/obtener_datos_ec2_boletas';

async function obtenerDatosBoletas() {
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

// Función para crear una tarjeta
function createCard(boleta) {
    const card = document.createElement('div');
    card.className = 'card mt-5';
    card.style.width = '18rem';
    card.style.height = '18rem';

    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    const cardTitle = document.createElement('h5');
    cardTitle.className = 'card-title';
    cardTitle.textContent = `Nro. Boleta: ${boleta.Numero_boleta}`;

    const cardTextFecha = document.createElement('p');
    cardTextFecha.className = 'card-text';
    cardTextFecha.textContent = `Fecha: ${boleta.fecha_emision}`;

    const cardTextNombre = document.createElement('p');
    cardTextNombre.className = 'card-text';
    cardTextNombre.textContent = `Nombre Comprador: ${boleta.cliente}`;

    const cardTextRUT = document.createElement('p');
    cardTextRUT.className = 'card-text';
    cardTextRUT.textContent = `Total: ${boleta.total}`;

    const button = document.createElement('a');
    button.className = 'btn btn-select';
    button.textContent = 'Seleccionar';
    button.setAttribute('href', `/devolucion/${boleta.numero_boleta}`);
    button.setAttribute('data-bs-toggle', 'modal');
    button.setAttribute('data-bs-target', '#myModal');
    button.setAttribute('data-numero_boleta', boleta.Numero_boleta);
    button.setAttribute('data-nombre_comprador', boleta.fecha_emision);
    button.setAttribute('data-rut_comprador', boleta.cliente);
    button.setAttribute('data-fecha', boleta.total);

    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardTextFecha);
    cardBody.appendChild(cardTextNombre);
    cardBody.appendChild(cardTextRUT);
    cardBody.appendChild(button);
    card.appendChild(cardBody);

    container.appendChild(card);
}

// Función para mostrar una página específica
function showPage(page) {
    container.innerHTML = '';
    const start = (page - 1) * cardsPerPage;
    const end = start + cardsPerPage;
    const pageData = data.slice(start, end);

    pageData.forEach(item => createCard(item));
    updatePagination(page);
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
        button.addEventListener('click', () => showPage(i));
        paginationContainer.appendChild(button);
    }
}

// Inicializar la primera página
obtenerDatosBoletas();

// Inicializar la primera página
showPage(currentPage);

// Función para navegar a la página anterior
function goToPreviousPage() {
    if (currentPage > 1) {
        currentPage--;
        showPage(currentPage);
    }
}

// Función para navegar a la página siguiente
function goToNextPage() {
    const totalPages = Math.ceil(data.length / cardsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        showPage(currentPage);
    }
}

// Agregar eventos de clic a los botones de flecha
document.getElementById('previousPageBtn').addEventListener('click', goToPreviousPage);
document.getElementById('nextPageBtn').addEventListener('click', goToNextPage);

// Validación de formulario
calendar.addEventListener("blur", function (event) {
    if (calendar.checkValidity() === false) {
        calendar.classList.remove("is-valid");
        calendar.classList.add("is-invalid");
    } else {
        calendar.classList.remove("is-invalid");
        calendar.classList.add("is-valid");
    }
});

calendar.addEventListener("keyup", function (event) {
    if (calendar.checkValidity() === false) {
        calendar.classList.remove("is-valid");
        calendar.classList.add("is-invalid");
    } else {
        calendar.classList.remove("is-invalid");
        calendar.classList.add("is-valid");
    }
});

calendar.addEventListener("change", function (event) {
    if (calendar.checkValidity() === false) {
        calendar.classList.remove("is-valid");
        calendar.classList.add("is-invalid");
    } else {
        calendar.classList.remove("is-invalid");
        calendar.classList.add("is-valid");
    }
});

input.addEventListener("blur", function (event) {
    if (input.checkValidity() === false) {
        input.classList.remove("is-valid");
        input.classList.add("is-invalid");
    } else {
        input.classList.remove("is-invalid");
        input.classList.add("is-valid");
    }
});

input.addEventListener("keyup", function (event) {
    if (input.checkValidity() === false) {
        input.classList.remove("is-valid");
        input.classList.add("is-invalid");
    } else {
        input.classList.remove("is-invalid");
        input.classList.add("is-valid");
    }
});

input.addEventListener("change", function (event) {
    if (input.checkValidity() === false) {
        input.classList.remove("is-valid");
        input.classList.add("is-invalid");
    } else {
        input.classList.remove("is-invalid");
        input.classList.add("is-valid");
    }
});

form.addEventListener("submit", function (event) {
    if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
    }
    form.classList.add("was-validated");
});

// Modal
$('#myModal').on('show.bs.modal', function (event) {
    const button = $(event.relatedTarget);
    const numero_boleta = button.data('numero_boleta');
    const fecha_emision = button.data('fecha_emision');
    const cliente = button.data('cliente');
    const total = button.data('total');

    const modal = $(this);
    // modal.find('.modal-title').text(`Boleta ${id}`);
    modal.find('.modal-body .card-title').text(`Nro. Boleta: ${numero_boleta}`);
    modal.find('.modal-body .card-text:eq(0)').text(`Nombre Comprador: ${cliente}`);
    modal.find('.modal-body .card-text:eq(1)').text(`Fecha Emision: ${fecha_emision}`);
    modal.find('.modal-body .card-text:eq(2)').text(`Total: ${total}`);    
    
    const devoLink = modal.find('#devoLink');
    devoLink.attr('href', `/devolucion/${numero_boleta}`);
});
