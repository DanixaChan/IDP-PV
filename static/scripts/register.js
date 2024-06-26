// register.js

document.getElementById("register-button").addEventListener("click", function() {
    console.log("Se hizo clic en el botón de registro.");
    var email = document.getElementById("InputEmail1").value;
    var password1 = document.getElementById("InputPassword1").value;
    var password2 = document.getElementById("InputPassword2").value;

    if (email === "") {
        alert("Por favor, introduce un correo electrónico.");
        return;
    }
    if (password1 === "") {
        alert("Por favor, introduce una contraseña.");
        return;
    }
    if (password2 === "") {
        alert("Por favor, confirma la contraseña.");
        return;
    }
    if (password1 !== password2) {
        alert("Las contraseñas no coinciden.");
        return;
    }
    
    var userCreatedAlert = document.getElementById('user-created');
    userCreatedAlert.classList.remove('d-none');
    
    setTimeout(function() {
        userCreatedAlert.classList.add('d-none');
    }, 3000);
});


