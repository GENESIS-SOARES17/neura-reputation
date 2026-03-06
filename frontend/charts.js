// charts.js
function renderCharts(data) {
    // Destrutura os dados recebidos
    const { age_score, activity_score, liquidity_score, governance_score, balance, tx_count } = data.analysis;

    // Gráfico de pizza: composição do score
    const ctx1 = document.getElementById('scoreChart').getContext('2d');
    new Chart(ctx1, {
        type: 'pie',
        data: {
            labels: ['Idade', 'Atividade', 'Liquidez', 'Governança'],
            datasets: [{
                data: [age_score, activity_score, liquidity_score, governance_score],
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
            }]
        },
        options: {
            plugins: {
                title: { display: true, text: 'Composição do Score', color: 'white' }
            }
        }
    });

    // Gráfico de barras: métricas on-chain
    const ctx2 = document.getElementById('volumeChart').getContext('2d');
    new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: ['Saldo (ETH)', 'Transações'],
            datasets: [{
                label: 'Valores',
                data: [balance, tx_count],
                backgroundColor: ['#42A5F5', '#66BB6A']
            }]
        },
        options: {
            plugins: {
                title: { display: true, text: 'Métricas On-Chain', color: 'white' }
            },
            scales: {
                y: { beginAtZero: true, ticks: { color: 'white' } },
                x: { ticks: { color: 'white' } }
            }
        }
    });

    // Gráfico de linha: histórico simulado (poderia ser real no futuro)
    const ctx3 = document.getElementById('activityChart').getContext('2d');
    new Chart(ctx3, {
        type: 'line',
        data: {
            labels: ['Ago', 'Set', 'Out', 'Nov', 'Dez'],
            datasets: [{
                label: 'Transações (últimos meses)',
                data: [2, 5, 3, 8, tx_count],
                borderColor: '#FFA726',
                backgroundColor: 'rgba(255, 167, 38, 0.2)',
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            plugins: {
                title: { display: true, text: 'Histórico de Atividade (simulado)', color: 'white' }
            },
            scales: {
                y: { beginAtZero: true, ticks: { color: 'white' } },
                x: { ticks: { color: 'white' } }
            }
        }
    });
}