document.addEventListener("DOMContentLoaded", function () {
    console.log("ListadoEjecutivo.js se está ejecutando correctamente.");
    const canvas = document.getElementById('pieChart');     

    if (!canvas) {
        console.error("No se encontró el elemento canvas con ID 'pieChart'");
        return;
    }    

    const ctx = canvas.getContext("2d");
    if (!ctx) {
        console.error("No se pudo obtener el contexto 2D del canvas.");
        return;
    }

    // Obtener los datos de la fila de totales
    const totalRow = document.querySelector('.total-row');
    if (!totalRow) {
        console.error("No se encontró la fila de totales.");
        return;
    }

    const totalCells = totalRow.querySelectorAll('td');
    if (totalCells.length < 7) {
        console.error("No hay suficientes celdas en la fila de totales.");
        return;
    }

    const totalData = {
        Deficiente: parseInt(totalCells[1].textContent.trim()) || 0,
        Insuficiente: parseInt(totalCells[2].textContent.trim()) || 0,
        Regular: parseInt(totalCells[3].textContent.trim()) || 0,
        Aceptable: parseInt(totalCells[4].textContent.trim()) || 0,
        Destacado: parseInt(totalCells[5].textContent.trim()) || 0,
        Excelente: parseInt(totalCells[6].textContent.trim()) || 0
    };

    const labels = ['Excelente', 'Destacado', 'Aceptable', 'Regular', 'Insuficiente', 'Deficiente'];
    const valores = [
        totalData.Excelente,
        totalData.Destacado,
        totalData.Aceptable,
        totalData.Regular,
        totalData.Insuficiente,
        totalData.Deficiente
    ];

    // Filtrar etiquetas y valores donde el valor sea mayor a 0
    const filteredLabels = [];
    const filteredData = [];
    const filteredColors = [];

    const colores = ['#227dba', '#a2cbf8', '#edef72', '#f28643', '#de4300', '#d30000'];

    valores.forEach((valor, index) => {
        if (valor > 0) {
            filteredLabels.push(labels[index]);
            filteredData.push(valor);
            filteredColors.push(colores[index]);
        }
    });

    // Crear el gráfico
    try {
        console.log("Creando gráfico...");
        window.myChart = new Chart(ctx, {
            type: 'pie', 
            data: {
                labels: filteredLabels,
                datasets: [{
                    data: filteredData,
                    backgroundColor: filteredColors,
                    borderColor: '#ffffff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'left',
                        labels: {
                            font: {
                                size: 30,
                                family: 'Arial, sans-serif',
                                weight: 'bold'
                            },
                            color: '#333',
                            boxWidth: 40,
                            padding: 15
                        }
                    },
                    datalabels: {
                        color: '#000',
                        font: {
                            weight: 'bold',
                            size: 18
                        },
                        anchor: 'end',
                        align: 'end',
                        offset: -55,
                        formatter: (value, context) => {
                            console.log("Valor:", value);
                            const data = context.chart.data.datasets[0].data;
                            const total = data.reduce((acc, val) => acc + val, 0);
                            const porcentaje = total ? Math.round((value / total) * 100) : 0;
                            return `${porcentaje}%`;
                        }
                    }
                }
            },
            plugins: [ChartDataLabels]
        });
        console.log("Gráfico inicializado correctamente.");
    } catch (error) {
        console.error("Error al inicializar el gráfico:", error);
    }
});

// Validación del formulario
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.filter');
    const fechaInicio = document.getElementById('fecha_inicio');
    const fechaFin = document.getElementById('fecha_fin');
    const sucursalInput = document.getElementById('sucursal');

    const codigosValidos = JSON.parse(document.getElementById('codigos-validos').textContent);

    form.addEventListener('submit', function (e) {
        const inicio = fechaInicio.value;
        const fin = fechaFin.value;
        const sucursal = sucursalInput.value.trim();

        if (inicio && fin && inicio > fin) {
            e.preventDefault();
            alert('La fecha de inicio no puede ser mayor que la fecha de fin.');
            return;
        }

        if (sucursal && !codigosValidos.includes(Number(sucursal))) {
            e.preventDefault();
            alert('El código de sucursal ingresado no es válido.');
            return;
        }
    });
});
document.addEventListener('DOMContentLoaded', function () {
    const filterInput = document.getElementById('ejecutivo-filter');
    const filterButton = document.getElementById('filter-button');
    const tableBody = document.getElementById('observations-body');

    if (!filterInput || !filterButton || !tableBody) {
        console.warn("Elementos de filtrado de observaciones no encontrados.");
        return;
    }

    filterButton.addEventListener('click', function () {
        const rutIngresado = filterInput.value.trim().toLowerCase();

        const filas = tableBody.querySelectorAll('tr');
        filas.forEach(fila => {
            const rutCliente = fila.querySelector('td')?.textContent.trim().toLowerCase() || '';
            const mostrar = rutCliente.includes(rutIngresado) || rutIngresado === '';
            fila.style.display = mostrar ? '' : 'none';
        });
    });
});
