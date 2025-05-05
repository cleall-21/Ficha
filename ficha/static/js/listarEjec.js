document.addEventListener("DOMContentLoaded", function () {
    console.log("ListadoEjecutivo.js se está ejecutando correctamente.");
    const canvas = document.getElementById('pieChart');     

    if (!canvas) {
        console.error("No se encontró el elemento canvas con ID 'pieChart'");
        return;
    }    
    console.log("canvas encontrado:", canvas);
    const ctx = canvas.getContext("2d");
    if (!ctx) {
        console.error("No se pudo obtener el contexto 2D del canvas.");
        return;
    }
    console.log("contexto 2D obtenido:", ctx);        
    
    // Inicializando el gráfico 
    try {
        console.log("Creando gráfico...");
        window.myChart = new Chart(ctx, {
            type: 'pie', 
            data: {
                labels: ['Excelente', 'Destacado', 'Aceptable', 'Regular', 'Insuficiente', 'Deficiente'],
                datasets: [{
                    data: [12, 8, 4, 5, 0, 0], //datos para el gráfico
                    backgroundColor: ['#1F618D', '#2980B9', '#5499C7', '#85C1E9', '#ADE6F1', '#D4E6F1'], //colores del grafico
                    borderColor: '#ffffff', //bordes blancos entre secciones
                    borderWidth: 2 //grosor del borde
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
                                size: 30,// Ajusta el tamaño de la fuente de las leyendas
                                family: 'Arial, sans-serif', // Cambia la fuente para mejor legibilidad
                                weight: 'bold' // Hace que las leyendas sean más legibles
                            },
                            color: '#333', 
                            boxWidth: 40,         //Aumenta el tamaño del color del recuadro
                            padding: 15
                        }
                    }
                }
            }
        });
        console.log("Gráfico inicializado correctamente.");
    } catch (error) {
        console.error("Error al inicializar el gráfico:", error);
    }
});