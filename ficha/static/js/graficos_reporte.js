document.addEventListener('DOMContentLoaded', function () {
    // === GRÁFICO PRINCIPAL ===
    const datos = JSON.parse(document.getElementById('datos-cumplimiento').textContent);
    const etiquetas = Object.keys(datos);
    const valores = etiquetas.map(etiqueta => datos[etiqueta]['% Cumplimiento']);

    const ctx = document.getElementById('barChartValidaciones').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: etiquetas,
            datasets: [{
                label: '% Cumplimiento',
                data: valores,
                backgroundColor: '#0a2a66',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: value => value + '%'
                    },
                    title: {
                        display: true,
                        text: 'Porcentaje de Cumplimiento'
                    }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: context => context.parsed.y + '%'
                    }
                },
                datalabels: {
                    color: '#fff',
                    font: {
                        weight: 'bold',
                        size: 18
                    },
                    anchor: 'end',
                    align: 'top',
                    offset: -150,
                    formatter: value => value + '%',
                }
            }
        },
        plugins: [ChartDataLabels]
    });

    // === GRÁFICOS POR CAMPO ===
    const datosPorCampo = JSON.parse(document.getElementById('datos-por-campo').textContent);
    const contenedor = document.getElementById('graficos-por-campo');
    const nombresLegibles = {
        // Formalidad
        respuesta_verificacion_laboral: "Verificación Laboral",
        respuesta_estado_situacion: "Estado de Situación",
        respuesta_acreditacion_ingresos: "Acreditación Ingresos",

        // Gestión Otorga
        respuesta_atribuciones: "Atribuciones",
        respuesta_constitucion_garantia: "Constitución Garantía",
        respuesta_condiciones_aprobacion: "Condiciones Aprobación",
        respuesta_cambio_evaAT: "Cambio Evaluación Automática",
        respuesta_deudas_vinculadas: "Deudas Vinculadas",

        // Depuración Antecedentes
        respuesta_ingresos_mensuales: "Ingresos Mensuales",
        respuesta_activo: "Activos",
        respuesta_dividendo_BCH: "Dividendo BCH",
        respuesta_arriendos: "Arriendos",
        respuesta_cuota_prestamo: "Cuota Préstamo",
        respuesta_renegociado: "Renegociado",
        respuesta_otros_egre: "Otros Egresos",
        respuesta_producto_compra_cartera: "Producto Compra Cartera",

        // Ingreso de Datos
        respuesta_actividad: "Actividad",
        respuesta_direccion_part: "Dirección Particular",
        respuesta_universidad: "Universidad",
        respuesta_fecha_in_empleo: "Fecha Ingreso Empleo",
        respuesta_nivel_educa: "Nivel Educacional",
        respuesta_nacionalidad: "Nacionalidad",
        respuesta_tipo_contrato: "Tipo Contrato",
        respuesta_tipo_renta: "Tipo Renta",
        respuesta_carrera_semestre: "Carrera/Semestre",
        respuesta_profesion: "Profesión",
        respuesta_estado_civil: "Estado Civil"
    };

    Object.entries(datosPorCampo).forEach(([pilar, campos], index) => {
        const seccion = document.createElement('div');
        seccion.classList.add('grafico-item');

        const titulo = document.createElement('h3');
        titulo.textContent = `${pilar}`;
        seccion.appendChild(titulo);

        const canvas = document.createElement('canvas');
        canvas.id = `grafico-${index}`;
        seccion.appendChild(canvas);
        contenedor.appendChild(seccion);

        const camposOrdenados = Object.keys(nombresLegibles).filter(campo => campo in campos);
        const etiquetasCampos = camposOrdenados.map(campo => nombresLegibles[campo] || campo);
        const sinError = camposOrdenados.map(campo => campos[campo]['% Cumplimiento']);
        const conError = camposOrdenados.map(campo => campos[campo]['% Error']);
        const cantidadEvaluada = camposOrdenados.map(campo => campos[campo]['Universo Revisado']);

        new Chart(canvas.getContext('2d'), {
            type: 'bar',
            data: {
                labels: etiquetasCampos,
                margin_bottom: '10px',
                datasets: [
                    {
                        label: '% Cumpl.',
                        data: sinError,
                        backgroundColor: '#0a2a66',
                        datalabels: {
                            display: true,
                            align: 'end',
                            anchor: 'end',
                            offset: -10,
                            formatter: (value, context) => {
                                const index = context.dataIndex;
                                return `${value}%\n(${cantidadEvaluada[index]})`;
                            },
                            backgroundColor: '#ffffff',
                            borderColor: '#0a2a66',
                            borderWidth: 1,
                            borderRadius: 4,
                            color: '#0a2a66',
                            font: {
                                weight: 'bold',
                                size: 12
                            },
                            padding: 4
                        }
                    },
                    {
                        label: '% Error',
                        data: conError,
                        backgroundColor: '#d9534f',
                        datalabels: {
                            display: true,
                            align: 'end',
                            anchor: 'end',
                            offset: -25,
                            formatter: value => value + '%',
                            color: '#fff',
                            font: {
                                weight: 'bold',
                                size: 14
                            }
                        }
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        stacked: true
                    },
                    y: {
                        stacked: true,
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: value => value + '%'
                        },
                        title: {
                            display: true,
                            text: 'Porcentaje'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: context => {
                                const index = context.dataIndex;
                                const evaluadas = cantidadEvaluada[index];
                                return `${context.dataset.label}: ${context.parsed.y}% (Evaluadas: ${evaluadas})`;
                            }
                        }
                    }
                }
            },
            plugins: [ChartDataLabels]
        });

    });
});