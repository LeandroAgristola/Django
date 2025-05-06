document.addEventListener('DOMContentLoaded', function () {
    // ===================== CLIENTES =====================
    const chartClientesCtx = document.getElementById('chartClientes').getContext('2d');
    let chartClientes;

    function cargarEstadisticasClientes(rango = '1m') {
        fetch(`/management/clientes/estadisticas/?rango=${rango}`)
            .then(res => res.json())
            .then(data => {
                const labels = ['Altas', 'Bajas'];
                const valores = [data.altas, data.bajas];

                if (chartClientes) {
                    chartClientes.data.datasets[0].data = valores;
                    chartClientes.update();
                } else {
                    chartClientes = new Chart(chartClientesCtx, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Cantidad',
                                data: valores,
                                backgroundColor: ['#4ade80', '#f87171']
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: { display: false },
                                title: { display: false }
                            }
                        }
                    });
                }

                document.getElementById('totalClientes').innerText =
                    `Altas: ${data.altas} | Bajas: ${data.bajas} | Total activos: ${data.total_activos}`;
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

    function cargarEstadisticasCalendario() {
        const url = `/management/calendario/estadisticas/?agrupacion=dia`;

        fetch(url)
            .then(res => res.json())
            .then(data => {
                const labels = data.labels;
                const ocupados = data.ocupados;
                const disponibles = data.disponibles;

                if (chartCalendario) {
                    chartCalendario.data.labels = labels;
                    chartCalendario.data.datasets[0].data = ocupados;
                    chartCalendario.data.datasets[1].data = disponibles;
                    chartCalendario.update();
                } else {
                    chartCalendario = new Chart(chartCalendarioCtx, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [
                                {
                                    label: 'Ocupados',
                                    data: ocupados,
                                    backgroundColor: '#60a5fa'
                                },
                                {
                                    label: 'Disponibles',
                                    data: disponibles,
                                    backgroundColor: '#fbbf24'
                                }
                            ]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: { position: 'top' },
                                title: { display: true, text: 'Turnos por Día (Últimos 30 días)' }
                            },
                            scales: {
                                y: { beginAtZero: true }
                            }
                        }
                    });
                }

                document.getElementById('totalCalendario').innerText =
                    `Totales → Ocupados: ${data.total_ocupados} | Disponibles: ${data.total_disponibles}`;
            });
    }

    cargarEstadisticasCalendario();
});