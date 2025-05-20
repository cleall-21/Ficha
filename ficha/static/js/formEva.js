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
                // Limpiar y actualizar el campo nombre_ejecutivo
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
                // Muestra resultados
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

    // Mostrar oportunidades al seleccionar código de sucursal
    codigoSucInput.addEventListener('change', () => {
        const formData = new FormData(form);
        ejecutivoSelect.innerHTML = '<option value="">---------</option>';
        ejecutivoSelect.disabled = true;
        cargarResultados(formData); // Muestra oportunidades y carga ejecutivos
    });

    // Filtrar por ejecutivo al seleccionarlo
    ejecutivoSelect.addEventListener('change', () => {
        const formData = new FormData(form);
        cargarResultados(formData); // Filtra resultados por ejecutivo
    });

    // También puedes actualizar ejecutivos si cambian las fechas
    [fechaInicioInput, fechaFinInput].forEach(input => {
        input.addEventListener('change', () => {
            const formData = new FormData(form);
            ejecutivoSelect.innerHTML = '<option value="">---------</option>';
            ejecutivoSelect.disabled = true;
            cargarResultados(formData); // Actualiza ejecutivos si cambia el rango de fechas
        });
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(form);
        cargarResultados(formData);
        activarPaginacion();
    });
});
document.addEventListener('DOMContentLoaded', function () {
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