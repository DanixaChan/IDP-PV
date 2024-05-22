fetch('http://44.205.221.190:8000/despachos/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Convertir la respuesta a JSON
    })
    .then(data => {
        if (typeof data === 'object' && !Array.isArray(data)) {
            console.log('Los datos son un objeto JSON:', data);
            // Aquí puedes procesar los datos como un objeto JSON
        } else {
            console.log('Los datos no son un objeto JSON:', data);
            // Aquí puedes manejar los datos de otra manera
        }
    })
    .catch(error => {
        console.error('Error al obtener los datos:', error);
    });
