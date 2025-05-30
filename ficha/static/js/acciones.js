document.addEventListener('DOMContentLoaded', function () {
    // Estado del usuario (no relacionado con evaluación)
    function setUserStatus(status) {
        var circle = document.getElementById('user-status');
        if (circle) {
            circle.classList.toggle('active', status === 'active');
            circle.classList.toggle('inactive', status !== 'active');
        }
    }

    setTimeout(() => setUserStatus('active'), 1000);

    // Delegación de eventos para botones que pueden cargarse dinámicamente
    document.body.addEventListener('click', function (e) {
        if (e.target.classList.contains('evaluar-btn')) {
            const rut = e.target.dataset.rut;

            fetch(`/obtener_oportunidad/${rut}/`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('No se pudo cargar la oportunidad.');
                    return;
                }

                // Rellenar campos del formulario
                document.getElementById('id_rut_cliente').value = data.rut_cliente;
                document.getElementById('id_nombre_ejec').value = data.nombre_ejec;
                document.getElementById('id_login_ejecutivo').value = data.login_ejecutivo;
                document.getElementById('id_rut_ejec').value = data.rut_ejec;
                document.getElementById('id_sucursal').value = data.sucursal;
                document.getElementById('id_codigo_sucursal').value = data.codigo_sucursal;
                document.getElementById('id_producto').value = data.producto;
                document.getElementById('id_monto_solicitado').value = data.monto_solicitado;
                document.getElementById('id_proceso_credito').value = data.proceso_credito;

                // Opcional: hacer scroll al formulario
                const formSection = document.querySelector('.tab-content');
                if (formSection) {
                    formSection.scrollIntoView({ behavior: 'smooth' });
                }
            });
        }
    });
});