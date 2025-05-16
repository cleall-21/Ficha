document.addEventListener('DOMContentLoaded', function() {
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
    setTimeout(function() {
        setUserStatus('active'); // 'inactive' para probar este estado
    }, 1000); 
});