document.addEventListener('DOMContentLoaded', function () {
    var tabs = document.querySelectorAll('.nav-link');
    var tabContents = document.querySelectorAll('.tab-pane');

    // Función para ocultar formularios vacíos
    function ocultarFormulariosVacios(tabId) {
        const tabPane = document.querySelector(tabId);
        if (!tabPane) return;

        const formularios = tabPane.querySelectorAll('.formset-form');
        formularios.forEach(formulario => {
            const inputs = formulario.querySelectorAll('input, select, textarea');
            let estaVacio = true;

            inputs.forEach(input => {
                if (input.type !== 'hidden' && input.value.trim() !== '') {
                    estaVacio = false;
                }
            });

            if (estaVacio) {
                formulario.style.display = 'none';
            }
        });
    }

    tabs.forEach(function (tab) {
        tab.addEventListener('click', function (event) {
            event.preventDefault();
            var targetId = tab.getAttribute('href');

            tabs.forEach(function (item) {
                item.classList.remove('active');
            });

            tabContents.forEach(function (content) {
                content.classList.remove('active');
            });

            tab.classList.add('active');
            document.querySelector(targetId).classList.add('active');

            ocultarFormulariosVacios(targetId);
        });
    });
    const activeTab = document.querySelector('.nav-link.active');
    if (activeTab) {
        ocultarFormulariosVacios(activeTab.getAttribute('href'));
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-filtros');
    const fechaInicio = document.getElementById('fecha-inicio');
    const fechaFin = document.getElementById('fecha-fin');
    const sucursal = document.getElementById('sucursal');
    const btnLimpiar = document.getElementById('btn-limpiar');
    const btnFiltrar = document.querySelector('.filtrar');

    let codigosValidos = [];
    const codigosJson = document.getElementById('codigos-validos-json');
    if (codigosJson) {
        codigosValidos = JSON.parse(codigosJson.textContent);
    }

    btnFiltrar.addEventListener('click', function (e) {
        e.preventDefault();

        const inicio = new Date(fechaInicio.value);
        const fin = new Date(fechaFin.value);
        const codigo = sucursal.value.trim();

        if (fechaInicio.value && fechaFin.value && inicio > fin) {
            alert('La fecha de inicio no puede ser posterior a la fecha de fin.');
            return;
        }

        if (codigo && codigosValidos.length && !codigosValidos.includes(codigo)) {
            alert('El código de sucursal ingresado no es válido.');
            return;
        }

        form.submit();
    });

    btnLimpiar.addEventListener('click', () => {
        fechaInicio.value = '';
        fechaFin.value = '';
        sucursal.value = '';
        form.submit();
    });
});