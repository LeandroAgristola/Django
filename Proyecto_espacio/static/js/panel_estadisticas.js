document.addEventListener('DOMContentLoaded', function () {
// ===================== CLIENTES =====================
const chartClientesCtx = document.getElementById('chartClientes').getContext('2d');
let chartClientes;

function cargarEstadisticasClientes() {
    fetch('/management/clientes/estadisticas/')
        .then(res => res.json())
        .then(data => {
            if (chartClientes) {
                chartClientes.data.labels = data.labels;
                chartClientes.data.datasets[0].data = data.altas;
                chartClientes.data.datasets[1].data = data.bajas;
                chartClientes.options.plugins.title.text = `Movimiento de Clientes - Año ${data.año}`;
                chartClientes.update();
            } else {
                chartClientes = new Chart(chartClientesCtx, {
                    type: 'line',
                    data: {
                        labels: data.labels,
                        datasets: [
                            {
                                label: 'Altas (Nuevos + Reactivaciones)',
                                data: data.altas,
                                borderColor: '#4ade80',
                                backgroundColor: 'rgba(74, 222, 128, 0.1)',
                                tension: 0.3,
                                fill: true,
                                borderWidth: 2
                            },
                            {
                                label: 'Bajas (Desactivados + Eliminados)',
                                data: data.bajas,
                                borderColor: '#f87171',
                                backgroundColor: 'rgba(248, 113, 113, 0.1)',
                                tension: 0.3,
                                fill: true,
                                borderWidth: 2
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { 
                                position: 'top',
                                labels: {
                                    usePointStyle: true,
                                }
                            },
                            title: { 
                                display: false, 
                            },
                            tooltip: {
                                callbacks: {
                                    footer: (context) => 
                                        `Total activos actual: ${data.total_activos}`
                                }
                            }
                        },
                        scales: {
                            y: { 
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Cantidad de clientes'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Meses del año'
                                }
                            }
                        }
                    }
                });
            }
        });
}

    document.querySelectorAll('#chartClientes').forEach(chart => {
        chart.closest('.col-md-6').querySelectorAll('[data-range]').forEach(btn => {
            btn.addEventListener('click', () => {
                const rango = btn.dataset.range;
                cargarEstadisticasClientes(rango);
            });
        });
    });

    cargarEstadisticasClientes();

// ===================== CALENDARIO =====================
    const chartCalendarioCtx = document.getElementById('chartCalendario').getContext('2d');
    let chartCalendario;

    function cargarEstadisticasCalendario(rango = 'actual') {
        fetch(`/management/calendario/estadisticas/?rango=${rango}`)
            .then(res => res.json())
            .then(data => {
                if (chartCalendario) {
                    chartCalendario.data.labels = data.labels;
                    chartCalendario.data.datasets = data.datasets;
                    chartCalendario.options.plugins.title.text = `Disponibilidad Diaria (${data.rango})`;
                    chartCalendario.update();
                } else {
                    chartCalendario = new Chart(chartCalendarioCtx, {
                        type: 'bar',
                        data: {
                            labels: data.labels,
                            datasets: data.datasets
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: { position: 'top' },
                                title: { 
                                    display: false, 
                                },
                                tooltip: {
                                    callbacks: {
                                        afterLabel: function(context) {
                                            const index = context.dataIndex;
                                            const total = data.maximos[index];
                                            const porcentaje = Math.round((context.raw / total) * 100);
                                            return `Máximo: ${total} (${porcentaje}%)`;
                                        }
                                    }
                                }
                            },
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    max: Math.max(...data.maximos) * 1.1,
                                    title: {
                                        display: true,
                                        text: 'Cantidad de Turnos'
                                    }
                                },
                                x: {
                                    title: {
                                        display: true,
                                        text: 'Días de la semana'
                                    }
                                }
                            }
                        }
                    });
                }
    
                document.getElementById('totalCalendario').innerText =
                    `Rango: ${data.rango} | Máximos: ${data.maximos.join(', ')}`;
            });
    }

    // Agregar botones de filtro
    document.querySelectorAll('#chartCalendario').forEach(chart => {
        chart.closest('.chart-panel').querySelectorAll('[data-range]').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('#chartCalendario').forEach(chart => {
                    chart.closest('.chart-panel').querySelectorAll('[data-range]').forEach(b => {
                        b.classList.remove('active');
                    });
                });
                this.classList.add('active');
                cargarEstadisticasCalendario(this.dataset.range);
            });
        });
    });

    cargarEstadisticasCalendario();

// ===================== PLANES =====================
const chartPlanesCtx = document.getElementById('chartPlanes').getContext('2d');
let chartPlanes;

function cargarEstadisticasPlanes() {
    fetch('/management/planes/estadisticas/')
        .then(res => res.json())
        .then(data => {
            if (chartPlanes) {
                chartPlanes.data.labels = data.labels;
                chartPlanes.data.datasets[0].data = data.data;
                chartPlanes.update();
            } else {
                chartPlanes = new Chart(chartPlanesCtx, {
                    type: 'pie',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Clientes',
                            data: data.data,
                            backgroundColor: [
                                '#3b82f6', '#10b981', '#f59e0b', '#ef4444', 
                                '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'
                            ],
                            borderWidth: 1,
                            borderColor: '#e3e5d7'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        devicePixelRatio: 2,
                        plugins: {
                            legend: { 
                                position: 'right',
                                align: 'center',
                                labels: {
                                    boxWidth: 12,
                                    padding: 16,
                                    font: {
                                        size: 11,
                                        family: "'Segoe UI', sans-serif"
                                    },
                                    usePointStyle: true
                                }
                            },
                            // Eliminamos el título del plugin
                            title: { 
                                display: false // Desactivamos el título interno
                            },
                            tooltip: {
                                callbacks: {
                                    footer: (context) => `Total: ${data.total} clientes`
                                },
                                bodyFont: {
                                    size: 15,
                                    family: "'Segoe UI', sans-serif"
                                }
                            }
                        },
                        layout: {
                            padding: {
                                top: 0,  // Reducimos el padding superior
                                right: 10,
                                bottom: 0, // Reducimos el padding inferior
                                left: 10
                            }
                        },
                        elements: {
                            arc: {
                                borderWidth: 1,
                                borderAlign: 'center'
                            }
                        }
                    }
                });
            }
        });
}

cargarEstadisticasPlanes();

// ===================== EVENTOS =====================
    const chartEventosCtx = document.getElementById('chartEventos').getContext('2d');
    let chartEventos;

    function cargarEstadisticasEventos(rango = '4') {
        fetch(`/management/eventos/estadisticas/?rango=${rango}`)
            .then(res => res.json())
            .then(data => {
                // Actualizar indicadores
                document.getElementById('cancelados').textContent = data.cancelados;
                document.getElementById('promedio').textContent = data.promedio_ocupacion;

                if (chartEventos) {
                    chartEventos.data.labels = data.labels;
                    chartEventos.data.datasets[0].data = data.cupos;
                    chartEventos.data.datasets[1].data = data.inscriptos;
                    chartEventos.update();
                } else {
                    chartEventos = new Chart(chartEventosCtx, {
                        type: 'bar',
                        data: {
                            labels: data.labels,
                            datasets: [
                                {
                                    label: 'Cupos Totales',
                                    data: data.cupos,
                                    backgroundColor: 'rgba(59, 130, 246, 0.7)',
                                    borderColor: 'rgba(59, 130, 246, 1)',
                                    borderWidth: 1
                                },
                                {
                                    label: 'Inscriptos',
                                    data: data.inscriptos,
                                    backgroundColor: 'rgba(16, 185, 129, 0.7)',
                                    borderColor: 'rgba(16, 185, 129, 1)',
                                    borderWidth: 1
                                }
                            ]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: true,
                            plugins: {
                                legend: { 
                                    position: 'top',
                                },
                                title: { 
                                    display: false, 
                                },
                                tooltip: {
                                    callbacks: {
                                        afterLabel: function(context) {
                                            const index = context.dataIndex;
                                            return `Ocupación: ${data.porcentajes[index]}%`;
                                        }
                                    }
                                }
                            },
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    title: {
                                        display: true,
                                        text: 'Cantidad de personas'
                                    }
                                }
                            }
                        }
                    });
                }
            });
    }

    // Event listeners para los botones de rango
    document.querySelectorAll('#chartEventos').forEach(chart => {
        chart.closest('.col-md-6').querySelectorAll('[data-range]').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('#chartEventos').forEach(chart => {
                    chart.closest('.col-md-6').querySelectorAll('[data-range]').forEach(b => {
                        b.classList.remove('active');
                    });
                });
                this.classList.add('active');
                cargarEstadisticasEventos(this.dataset.range);
            });
        });
    });

    // Cargar inicialmente
    cargarEstadisticasEventos();

});