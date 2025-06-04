document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('sucursalForm');
    const loader = document.getElementById('loader');
    const resultados = document.getElementById('resul');
    const ejecutivoSelect = document.getElementById('id_nombre_ejecutivo');
    const codigoSucInput = document.getElementById('id_codigo_suc');
    const fechaInicioInput = document.getElementById('id_fecha_inicio');
    const fechaFinInput = document.getElementById('id_fecha_fin');

    function cargarResultados(formData, page = 1) {
        loader.style.display = 'block';
        setTimeout(() => loader.classList.add('visible'), 10);
        resultados.style.display = 'none';

        const url = `/buscar_oportunidad/?page=${page}`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.errors ? JSON.stringify(data.errors) : 'Respuesta no válida');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.ejecutivos) {
                ejecutivoSelect.innerHTML = '<option value="">---------</option>';
                if (data.ejecutivos.length > 0) {
                    data.ejecutivos.forEach(nombre => {
                        const option = document.createElement('option');
                        option.value = nombre;
                        option.textContent = nombre;
                        ejecutivoSelect.appendChild(option);
                    });
                    ejecutivoSelect.disabled = false;
                } else {
                    ejecutivoSelect.disabled = true;
                }
            } else if (data.html) {
                setTimeout(() => {
                    resultados.innerHTML = data.html;
                    loader.classList.remove('visible');
                    setTimeout(() => loader.style.display = 'none', 500);
                    resultados.style.display = 'block';
                    activarPaginacion();
                }, 1000);
            }
        })
        .catch(error => {
            resultados.innerHTML = '<p>Codigo de sucursal no existe.</p>';
            loader.classList.remove('visible');
            setTimeout(() => loader.style.display = 'none', 500);
            resultados.style.display = 'block';
            console.error('Error:', error);
        });
    }
    function limpiarFormulario() {
        form.reset();

        resultados.innerHTML = '';
        resultados.style.display = 'none';

        ejecutivoSelect.innerHTML = '<option value="">---------</option>';
        ejecutivoSelect.disabled = true;

        loader.classList.remove('visible');
        loader.style.display = 'none';
    }
    document.getElementById('btn-limpiar').addEventListener('click', limpiarFormulario);


    function activarPaginacion() {
        document.querySelectorAll('.pagina').forEach(link => {
            link.addEventListener('click', function (e) {
                e.preventDefault();
                const page = this.getAttribute('data-page');
                const formData = new FormData(form);
                cargarResultados(formData, page);
            });
        });
    }

    codigoSucInput.addEventListener('change', () => {
        const formData = new FormData(form);
        ejecutivoSelect.innerHTML = '<option value="">---------</option>';
        ejecutivoSelect.disabled = true;

    });

    ejecutivoSelect.addEventListener('change', () => {
        const formData = new FormData(form);
        cargarResultados(formData);
    });

    [fechaInicioInput, fechaFinInput].forEach(input => {
        input.addEventListener('change', () => {
            const formData = new FormData(form);
            ejecutivoSelect.innerHTML = '<option value="">---------</option>';
            ejecutivoSelect.disabled = true;
        });
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(form);
        cargarResultados(formData);
        activarPaginacion();
    });

    // Tabs
    var tabs = document.querySelectorAll('.nav-link');
    var tabContents = document.querySelectorAll('.tab-pane');

    tabs.forEach(function (tab) {
        tab.addEventListener('click', function (event) {
            event.preventDefault();
            var target = document.querySelector(tab.getAttribute('href'));

            tabs.forEach(function (item) {
                item.classList.remove('active');
            });

            tabContents.forEach(function (content) {
                content.classList.remove('active');
            });

            tab.classList.add('active');
            target.classList.add('active');
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    function toggleCampoPorRespuesta(select) {
        const value = select.value.trim().toLowerCase();
        const container = select.closest('.form-group');
        if (!container) return;

        const tipoError = container.querySelector('.tipo-error');
        const observacion = container.querySelector('.observacion');

        if (tipoError && observacion) {
            const ocultar = value === 'sin error' || value === 'n/a';
            tipoError.style.display = ocultar ? 'none' : '';
            observacion.style.display = ocultar ? 'none' : '';
        }
    }

    function toggleCompraCartera(campo) {
        const container = campo.closest('.formset-form');
        const campos = container?.querySelector('.campos-compra-cartera');
        if (!campos) return;

        const valor = campo.type === 'checkbox' ? campo.checked : campo.value;
        const esVerdadero = ['true', '1', 'on'].includes(String(valor).toLowerCase()) || valor === true;

        campos.style.display = esVerdadero ? 'block' : 'none';

        // Si no corresponde compra cartera, marcar campos como "N/A"
        if (!esVerdadero) {
            campos.querySelectorAll('select').forEach(input => {
                if (input.type === 'checkbox' || input.type === 'radio') {
                    input.checked = false;
                } else {
                    input.value = 'N/A';
                }
            });
        }
    }

    document.querySelectorAll('select').forEach(select => {
        toggleCampoPorRespuesta(select);
        select.addEventListener('change', () => toggleCampoPorRespuesta(select));
    });

    document.querySelectorAll('[name$="corresponde_compra_cartera"]').forEach(campo => {
        toggleCompraCartera(campo);
        campo.addEventListener('change', () => toggleCompraCartera(campo));
    });
});
