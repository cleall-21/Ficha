document.addEventListener('DOMContentLoaded', () => {
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const calcularResumenBtn = document.getElementById('calcular-resumen');
    const tablaDetalles = document.getElementById('tabla-detalles');

    // Cargar resumen por sucursal
    async function cargarResumenSucursales() {
        try {
            const response = await fetch('/detalle-evaluaciones/');
            if (!response.ok) throw new Error('Error al obtener los detalles');

            const detalles = await response.json();

            tablaDetalles.innerHTML = '';

            if (detalles.length === 0) {
                tablaDetalles.innerHTML = `
                    <tr>
                        <td colspan="6" style="text-align: center; color: gray;">
                            No hay datos disponibles para mostrar.
                        </td>
                    </tr>`;
                return;
            }

            detalles.forEach(det => {
                const row = document.createElement('tr');
                row.dataset.codigo = det.codigo_sucursal;
                row.innerHTML = `
                    <td>${det.codigo_sucursal}</td>
                    <td>${det.nombre_sucursal}</td>
                    <td>${det.promedio_notas}</td>
                    <td>
                        <input type="number" step="0.1" name="nota_automatica" value="${det.nota_automatica}" min="1" max="7" />
                    </td>
                    <td>${det.nota_final}</td>
                    <td>${det.clasificacion_final}</td>
                `;
                tablaDetalles.appendChild(row);
            });
        } catch (error) {
            console.error('Error al cargar resumen de sucursales:', error);
            tablaDetalles.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; color: red;">
                        Error al cargar los datos. Intenta nuevamente más tarde.
                    </td>
                </tr>`;
        }
    }

    // Calcular resumen por sucursal
    calcularResumenBtn.addEventListener('click', async () => {
        const filas = document.querySelectorAll('#tabla-detalles tr');

        for (const fila of filas) {
            const codigo = fila.dataset.codigo;
            const input = fila.querySelector('input[name="nota_automatica"]');
            if (!codigo || !input) continue;

            const nota = parseFloat(input.value);
            if (isNaN(nota) || nota < 1 || nota > 7) {
                alert(`Nota inválida para sucursal ${codigo}. Debe estar entre 1.0 y 7.0`);
                input.focus();
                return;
            }

            try {
                const response = await fetch(`/detalle-evaluaciones/${codigo}/calcular/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({ nota_automatica: nota })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error(`Error al actualizar sucursal ${codigo}:`, errorData);
                }
            } catch (error) {
                console.error(`Error de red al actualizar sucursal ${codigo}:`, error);
            }
        }

        alert('Resumen actualizado.');
        cargarResumenSucursales();
    });

    // Cargar resumen al inicio
    cargarResumenSucursales();
});