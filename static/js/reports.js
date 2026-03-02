// static/js/reports.js
document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const periodSelect = document.getElementById('period-select');
    const exportBtn = document.getElementById('export-btn');
    const exportDropdown = document.getElementById('export-dropdown');
    const loadingEl = document.getElementById('loading');
    const reportCards = document.getElementById('report-cards');
    const tableBody = document.getElementById('report-table-body');
    
    // Variáveis para os gráficos
    let lineChart, pieChart;
    
    // Carrega dados iniciais
    carregarDados('month');
    
    // Event Listeners
    periodSelect.addEventListener('change', function() {
        carregarDados(this.value);
    });
    
    // Toggle dropdown de exportação
    exportBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        exportDropdown.classList.toggle('hidden');
    });
    
    // Fecha dropdown ao clicar fora
    document.addEventListener('click', function() {
        exportDropdown.classList.add('hidden');
    });
    
    // Opções de exportação
    document.querySelectorAll('.export-option').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const format = this.dataset.format;
            const period = periodSelect.value;
            exportarRelatorio(format, period);
            exportDropdown.classList.add('hidden');
        });
    });
    
    // Função principal para carregar dados
    function carregarDados(period) {
        // Mostra loading
        loadingEl.classList.remove('hidden');
        reportCards.classList.add('opacity-50');
        
        fetch(`/relatorios/api/dados/?period=${period}`)
            .then(response => response.json())
            .then(data => {
                // Atualiza cards
                atualizarCards(data);
                
                // Atualiza gráficos
                atualizarGraficos(data.dados_graficos);
                
                // Atualiza tabela
                atualizarTabela(data.relatorio_detalhado);
                
                // Esconde loading
                loadingEl.classList.add('hidden');
                reportCards.classList.remove('opacity-50');
            })
            .catch(error => {
                console.error('Erro ao carregar dados:', error);
                loadingEl.classList.add('hidden');
                reportCards.classList.remove('opacity-50');
                mostrarErro('Erro ao carregar relatórios. Tente novamente.');
            });
    }
    
    // Atualiza os cards de relatório
    function atualizarCards(data) {
        const cards = `
            <!-- Card 1 - Vendas por Marca -->
            <div class="glass rounded-2xl p-6 neon-border">
                <div class="flex items-center justify-between mb-4">
                    <h4 class="font-medium text-slate-300">Vendas por Marca</h4>
                    <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewbox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                    </svg>
                </div>
                <div class="space-y-3">
                    ${data.vendas_por_marca.map(item => `
                        <div class="flex items-center justify-between">
                            <span class="text-sm text-slate-400">${item.marca}</span>
                            <span class="text-sm text-cyan-400">${item.vendas} vendas</span>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <!-- Card 2 - Performance Vendedores -->
            <div class="glass rounded-2xl p-6 neon-border">
                <div class="flex items-center justify-between mb-4">
                    <h4 class="font-medium text-slate-300">Performance Vendedores</h4>
                    <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewbox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                </div>
                <div class="space-y-3">
                    ${data.performance_vendedores.map(item => `
                        <div class="flex items-center justify-between">
                            <span class="text-sm text-slate-400">${item.nome}</span>
                            <span class="text-sm text-green-400">R$ ${formatarMoeda(item.valor)}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <!-- Card 3 - Métricas Gerais -->
            <div class="glass rounded-2xl p-6 neon-border">
                <div class="flex items-center justify-between mb-4">
                    <h4 class="font-medium text-slate-300">Métricas Gerais</h4>
                    <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewbox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                </div>
                <div class="space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-sm text-slate-400">Ticket Médio</span>
                        <span class="text-sm text-cyan-400">R$ ${formatarMoeda(data.metricas_gerais.ticket_medio)}</span>
                    </div>
                    <div class="flex items-center justify-between">
                        <span class="text-sm text-slate-400">Taxa Conversão</span>
                        <span class="text-sm text-cyan-400">${data.metricas_gerais.taxa_conversao}%</span>
                    </div>
                    <div class="flex items-center justify-between">
                        <span class="text-sm text-slate-400">Leads/Mês</span>
                        <span class="text-sm text-cyan-400">${data.metricas_gerais.leads_mes}</span>
                    </div>
                </div>
            </div>
        `;
        
        reportCards.innerHTML = cards;
    }
    
    // Atualiza os gráficos
    function atualizarGraficos(dados) {
        // Destrói gráficos existentes
        if (lineChart) lineChart.destroy();
        if (pieChart) pieChart.destroy();
        
        // Gráfico de linhas
        const lineCtx = document.getElementById('line-chart').getContext('2d');
        lineChart = new Chart(lineCtx, {
            type: 'line',
            data: dados.line_chart,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#94a3b8' }
                    }
                },
                scales: {
                    y: {
                        grid: { color: 'rgba(148, 163, 184, 0.1)' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { color: 'rgba(148, 163, 184, 0.1)' },
                        ticks: { color: '#94a3b8' }
                    }
                }
            }
        });
        
        // Gráfico de pizza
        const pieCtx = document.getElementById('pie-chart').getContext('2d');
        pieChart = new Chart(pieCtx, {
            type: 'pie',
            data: dados.pie_chart,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#94a3b8' }
                    }
                }
            }
        });
    }
    
    // Atualiza a tabela de relatório detalhado
    function atualizarTabela(dados) {
        let html = '';
        
        dados.forEach(item => {
            const corCrescimento = item.crescimento >= 0 ? 'text-green-400' : 'text-red-400';
            const sinal = item.crescimento >= 0 ? '+' : '';
            
            html += `
                <tr class="table-row border-b border-slate-700/50">
                    <td class="py-4 font-medium">${item.periodo}</td>
                    <td class="py-4 text-slate-300">${item.vendas}</td>
                    <td class="py-4 text-cyan-400">R$ ${formatarMoeda(item.receita)}</td>
                    <td class="py-4 text-slate-300">R$ ${formatarMoeda(item.comissoes)}</td>
                    <td class="py-4"><span class="${corCrescimento}">${sinal}${item.crescimento}%</span></td>
                </tr>
            `;
        });
        
        tableBody.innerHTML = html;
    }
    
    // Exporta relatório
    function exportarRelatorio(format, period) {
        window.location.href = `/relatorios/api/exportar/?format=${format}&period=${period}`;
    }
    
    // Formata moeda
    function formatarMoeda(valor) {
        return valor.toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }
    
    // Mostra mensagem de erro
    function mostrarErro(mensagem) {
        const toast = document.createElement('div');
        toast.className = 'fixed bottom-4 right-4 bg-red-600 text-white px-6 py-3 rounded-lg shadow-lg z-50';
        toast.textContent = mensagem;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
});