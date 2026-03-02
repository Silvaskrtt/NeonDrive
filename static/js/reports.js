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
    
    // Variáveis de exportação (globais para acesso das funções do modal)
    window.selectedFormat = 'excel';
    window.selectedPeriod = 'month';
    
    // Carrega dados iniciais
    carregarDados('month');
    
    // Event Listeners
    periodSelect.addEventListener('change', function() {
        carregarDados(this.value);
        window.selectedPeriod = this.value;
    });
    
    // Toggle dropdown de exportação
    exportBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        exportDropdown.classList.toggle('hidden');
    });
    
    // Fecha dropdown ao clicar fora
    document.addEventListener('click', function(e) {
        if (!exportBtn.contains(e.target) && !exportDropdown.contains(e.target)) {
            exportDropdown.classList.add('hidden');
        }
    });
    
    // Opções de exportação do dropdown
    document.querySelectorAll('.export-option').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const format = this.dataset.format;
            const period = periodSelect.value;
            
            // Abre o modal com o formato pré-selecionado
            openExportModal(format, period);
            exportDropdown.classList.add('hidden');
        });
    });
    
    // Função principal para carregar dados
    function carregarDados(period) {
        loadingEl.classList.remove('hidden');
        reportCards.classList.add('opacity-50');
        
        fetch(`/relatorios/api/dados/?period=${period}`)
            .then(response => response.json())
            .then(data => {
                atualizarCards(data);
                atualizarGraficos(data.dados_graficos);
                atualizarTabela(data.relatorio_detalhado);
                loadingEl.classList.add('hidden');
                reportCards.classList.remove('opacity-50');
            })
            .catch(error => {
                console.error('Erro:', error);
                loadingEl.classList.add('hidden');
                reportCards.classList.remove('opacity-50');
                mostrarErro('Erro ao carregar relatórios');
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

// ==============================================
// FUNÇÕES GLOBAIS DO MODAL DE EXPORTAÇÃO
// ==============================================

// Abre o modal de exportação
function openExportModal(format = 'excel', period = 'month') {
    const modal = document.getElementById('export-modal');
    if (!modal) return;
    
    // Reseta mensagens
    document.getElementById('success-message').classList.remove('show');
    document.getElementById('error-message').classList.remove('show');
    document.getElementById('progress-bar').classList.remove('active');
    
    // Seleciona o formato
    window.selectedFormat = format;
    window.selectedPeriod = period;
    
    // Atualiza UI dos formatos
    document.querySelectorAll('.export-option-card').forEach(card => {
        if (card.dataset.format === format) {
            card.classList.add('selected');
        } else {
            card.classList.remove('selected');
        }
    });
    
    // Atualiza UI dos períodos
    document.querySelectorAll('.period-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Marca o botão de período correto
    const periodBtn = Array.from(document.querySelectorAll('.period-btn')).find(
        btn => btn.getAttribute('onclick')?.includes(period)
    );
    if (periodBtn) {
        periodBtn.classList.add('active');
    }
    
    modal.classList.add('active');
}

// Fecha o modal de exportação
function closeExportModal() {
    const modal = document.getElementById('export-modal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// Seleciona formato
function selectFormat(format) {
    window.selectedFormat = format;
    document.querySelectorAll('.export-option-card').forEach(card => {
        if (card.dataset.format === format) {
            card.classList.add('selected');
        } else {
            card.classList.remove('selected');
        }
    });
}

// Seleciona período
function selectPeriod(period, event) {
    window.selectedPeriod = period;
    document.querySelectorAll('.period-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}

// Confirma exportação
function confirmExport() {
    const progressBar = document.getElementById('progress-bar');
    const progressFill = document.getElementById('progress-fill');
    const successMsg = document.getElementById('success-message');
    const errorMsg = document.getElementById('error-message');
    
    // Reseta mensagens
    successMsg.classList.remove('show');
    errorMsg.classList.remove('show');
    
    // Mostra barra de progresso
    progressBar.classList.add('active');
    progressFill.style.width = '0%';
    
    // URL de exportação
    const url =  `${window.location.origin}/relatorios/api/exportar/?format=${window.selectedFormat}&period=${window.selectedPeriod}`;
    console.log('Exportando:', url);
    
    // Pega o token CSRF do cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    // Faz a requisição fetch para obter o arquivo
    fetch(url, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        }
    })
    .then(async response => {
        console.log('Status da resposta:', response.status);
        console.log('Headers:', response.headers);
        
        if (response.status === 403) {
            throw new Error('Erro de autenticação. Faça login novamente.');
        }
        
        if (!response.ok) {
            const text = await response.text();
            throw new Error(`Erro ${response.status}: ${text}`);
        }
        
        const contentType = response.headers.get('content-type');
        console.log('Content-Type:', contentType);
        
        // Se for JSON, provavelmente é erro
        if (contentType && contentType.includes('application/json')) {
            const data = await response.json();
            throw new Error(data.error || 'Erro na exportação');
        }
        
        // Obtém o blob do arquivo
        const blob = await response.blob();
        console.log('Blob recebido:', blob.type, blob.size, 'bytes');
        
        if (blob.size === 0) {
            throw new Error('Arquivo vazio recebido');
        }
        
        // Determina o nome do arquivo
        const dataAtual = new Date().toISOString().slice(0,10);
        let nomeArquivo = `relatorio_vendas_${dataAtual}`;
        
        if (window.selectedFormat === 'excel') {
            nomeArquivo += '.xlsx';
        } else if (window.selectedFormat === 'csv') {
            nomeArquivo += '.csv';
        } else if (window.selectedFormat === 'pdf') {
            nomeArquivo += '.pdf';
        }
        
        // Cria URL do blob e faz download
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = nomeArquivo;
        document.body.appendChild(link);
        link.click();
        
        // Limpa
        setTimeout(() => {
            window.URL.revokeObjectURL(downloadUrl);
            link.remove();
        }, 100);
        
        // Progresso 100%
        progressFill.style.width = '100%';
        
        // Mostra mensagem de sucesso
        setTimeout(() => {
            progressBar.classList.remove('active');
            successMsg.classList.add('show');
            
            // Fecha o modal após 2 segundos
            setTimeout(() => {
                closeExportModal();
            }, 2000);
        }, 500);
    })
    .catch(error => {
        console.error('Erro no download:', error);
        
        // Para a animação
        progressBar.classList.remove('active');
        
        // Mostra mensagem de erro específica
        errorMsg.textContent = `❌ ${error.message}`;
        errorMsg.classList.add('show');
        
        // Esconde a mensagem após 5 segundos
        setTimeout(() => {
            errorMsg.classList.remove('show');
        }, 5000);
    });
}

function exportarFallback(format, period) {
    const url = `/relatorios/api/exportar/?format=${format}&period=${period}`;
    console.log('Fallback export:', url);
    window.location.href = url;
}

// Modifique o handler do dropdown para oferecer as duas opções
document.querySelectorAll('.export-option').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.stopPropagation();
        const format = this.dataset.format;
        const period = periodSelect.value;
        
        // Pergunta ao usuário qual método usar
        if (confirm('Usar método de download alternativo?')) {
            exportarFallback(format, period);
        } else {
            openExportModal(format, period);
        }
        exportDropdown.classList.add('hidden');
    });
});

// Fecha modal com ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeExportModal();
    }
});

// Fecha modal clicando fora
document.addEventListener('click', function(e) {
    const modal = document.getElementById('export-modal');
    const exportCard = document.querySelector('.export-card');
    
    if (modal && modal.classList.contains('active') && 
        exportCard && !exportCard.contains(e.target)) {
        closeExportModal();
    }
});