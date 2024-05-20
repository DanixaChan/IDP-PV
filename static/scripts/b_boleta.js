const input = document.querySelector(".form-control");
const calendar = document.getElementById("calend-compra");
const form = document.getElementById("form-filt");

const container = document.getElementById('div-grid-bol');
const paginationContainer = document.getElementById('pagination');
const cardsPerPage = 12;
let currentPage = 1;

// Datos de ejemplo
const data = [];
for (let i = 1; i <= 100; i++) {
  data.push({ id: i, fecha: '2024-05-18' });
}

// Función para crear una tarjeta
function createCard(id, fecha) {
  const card = document.createElement('div');
  card.className = 'card mt-5';
  card.style.width = '18rem';
  card.style.height = '12rem';

  const cardBody = document.createElement('div');
  cardBody.className = 'card-body';

  const cardTitle = document.createElement('h5');
  cardTitle.className = 'card-title';
  cardTitle.textContent = `Id: ${id}`;

  const cardText = document.createElement('p');
  cardText.className = 'card-text';
  cardText.textContent = `Fecha: ${fecha}`;

  const button = document.createElement('a');
  button.className = 'btn btn-select';
  button.textContent = 'Seleccionar';
  button.setAttribute('data-bs-toggle', 'modal');
  button.setAttribute('data-bs-target', '#myModal');

  cardBody.appendChild(cardTitle);
  cardBody.appendChild(cardText);
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

  pageData.forEach(item => createCard(item.id, item.fecha));
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
