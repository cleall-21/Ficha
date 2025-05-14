document.addEventListener('DOMContentLoaded', function() {
    var limpiarBtn = document.getElementById('limpiarBtn');
    var resul = document.getElementById('resul');
    var sucursalForm = document.getElementById('sucursalForm');

    if (limpiarBtn && resul && sucursalForm ) {
        limpiarBtn.addEventListener('click', function() {
            sucursalForm.reset(); // Restablece el formulario
            resul.innerHTML = ''; // Limpia el contenido de resul
        });

    }
     // Función para cambiar el color del círculo según el estado del usuario
     function setUserStatus(status) {
        var circle = document.getElementById('user-status');
        if (status === 'active') {
            circle.classList.remove('inactive');
            circle.classList.add('active');
        } else if (status === 'inactive') {
            circle.classList.remove('active');
            circle.classList.add('inactive');
        }
    }

    // Simulación de cambio de estado del usuario
    // Puedes reemplazar esto con la lógica real de tu aplicación
    setTimeout(function() {
        setUserStatus('active'); // Cambia a 'inactive' para probar el estado inactivo
    }, 1000); 
});