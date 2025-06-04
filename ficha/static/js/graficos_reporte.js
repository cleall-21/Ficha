document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('barChartValidaciones').getContext('2d');
    const barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Formalidad', 'Gestión de Otorgamiento', 'Depuración de Antecedentes', 'Ingreso de Datos'],
            datasets: [{
                label: '% Cumplimiento',
                data: [73, 93, 92, 90],
                backgroundColor: '#0a2a66', // Azul oscuro
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    },
                    title: {
                        display: true,
                        text: 'Porcentaje de Cumplimiento'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.parsed.y + '%';
                        }
                    }
                },
                datalabels: {
                    anchor: 'end',
                    align: 'top',
                    formatter: function(value) {
                        return value + '%';
                    },
                    color: '#0a2a66',
                    font: {
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: [ChartDataLabels]
    });
});