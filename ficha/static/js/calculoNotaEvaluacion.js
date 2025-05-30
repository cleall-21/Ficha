document.addEventListener('DOMContentLoaded', () => {
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const filtroForm = document.getElementById('filtro-form');
    const listaEvaluaciones = document.getElementById('evaluaciones-lista');
    const calcularTodasBtn = document.getElementById('calcular-todas');

    // Crear elemento de evaluación
    function crearElementoEvaluacion(eva) {
        const li = document.createElement('li');
        li.dataset.idEvaluacion = eva.id_evaluacion;
        li.innerHTML = `
            Fecha: ${eva.fecha} - 
            ID: ${eva.id_evaluacion} - 
            Rut: ${eva.rut_cliente} - 
            Ejecutivo: ${eva.login_ejecutivo} - 
            Sucursal: ${eva.codigo_sucursal} - 
            Nota: <span id="nota-${eva.id_evaluacion}">${eva.nota_final}</span> - 
            <span id="clasificacion-${eva.id_evaluacion}">${eva.clasificacion}</span>
        `;
        return li;
    }

    // Limpiar lista de evaluaciones
    function limpiarEvaluaciones() {
        listaEvaluaciones.innerHTML = '';
    }

    // Cargar evaluaciones filtradas
    filtroForm.addEventListener('submit', function (e) {
        e.preventDefault();
        limpiarEvaluaciones();

        const fechaInicio = document.getElementById('fecha_inicio').value;
        const fechaFin = document.getElementById('fecha_fin').value;
        const sucursal = document.getElementById('sucursal').value;

        const params = new URLSearchParams();
        if (fechaInicio) params.append('fecha__gte', fechaInicio);
        if (fechaFin) params.append('fecha__lte', fechaFin);
        if (sucursal) params.append('codigo_sucursal', sucursal);

        const url = `/evaluaciones/?${params.toString()}`;
        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error('Error al obtener evaluaciones');
                return response.json();
            })
            .then(data => {
                if (data.length === 0) {
                    listaEvaluaciones.innerHTML = '<li>No se encontraron evaluaciones.</li>';
                    return;
                }
                data.forEach(eva => {
                    listaEvaluaciones.appendChild(crearElementoEvaluacion(eva));
                });
            })
            .catch(error => {
                console.error('Error al cargar evaluaciones:', error);
                alert('Hubo un problema al cargar las evaluaciones.');
            });
    });

    // Limpiar evaluaciones al resetear el formulario
    filtroForm.addEventListener('reset', limpiarEvaluaciones);

    // Calcular todas las notas individuales
    calcularTodasBtn.addEventListener('click', async () => {
        const items = document.querySelectorAll('#evaluaciones-lista li');
        for (const li of items) {
            const id = li.dataset.idEvaluacion;
            try {
                const response = await fetch(`/evaluaciones/${id}/calcular/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({})
                });
                if (!response.ok) throw new Error('Error en el cálculo');
                const data = await response.json();
                document.getElementById(`nota-${id}`).textContent = data.nota_final;
                document.getElementById(`clasificacion-${id}`).textContent = data.clasificacion;
            } catch (error) {
                console.error(`Error al calcular la nota para ID ${id}:`, error);
            }
        }
    });
});