document.addEventListener('DOMContentLoaded', function () {
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

    // Carga inicial
    cargarEstadisticasClientes();

    // Botones de rango con feedback visual
    document.querySelectorAll('[data-range]').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('[data-range]').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const rango = btn.dataset.range;
            cargarEstadisticasClientes(rango);
        });
    });
});
