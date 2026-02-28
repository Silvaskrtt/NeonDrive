// Dashboard JavaScript específico

document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

function initializeDashboard() {
    console.log('Dashboard inicializado');
    
    // Inicializar componentes
    initializeSidebar();
    initializeCharts();
    initializeStatsCounters();
    setupEventListeners();
}

// Sidebar Functions
function initializeSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    const toggleBtn = document.getElementById('sidebar-toggle');
    
    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleSidebar);
    }
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    
    if (sidebar && overlay) {
        sidebar.classList.toggle('-translate-x-full');
        overlay.classList.toggle('hidden');
        
        // Prevenir scroll do body quando sidebar estiver aberta no mobile
        if (!overlay.classList.contains('hidden')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'auto';
        }
    }
}

// Chart Functions
function initializeCharts() {
    // Animação das barras do gráfico
    const chartBars = document.querySelectorAll('[class*="bg-gradient-to-t"]');
    
    chartBars.forEach((bar, index) => {
        // Adicionar delay na animação baseado no índice
        bar.style.animation = `bar-rise 0.5s ease-out ${index * 0.1}s both`;
        
        // Adicionar tooltip com valor
        const height = bar.style.height;
        const value = parseInt(height);
        
        bar.addEventListener('mouseenter', function(e) {
            showTooltip(e, `R$ ${value * 1000}`);
        });
        
        bar.addEventListener('mouseleave', hideTooltip);
    });
}

// Stats Counter Animation
function initializeStatsCounters() {
    const statValues = document.querySelectorAll('.text-3xl.font-bold');
    
    statValues.forEach(stat => {
        const value = stat.innerText;
        
        // Verificar se é um valor monetário
        if (value.includes('R$')) {
            animateMoneyValue(stat, value);
        } 
        // Verificar se é um número
        else if (!isNaN(value.replace(',', ''))) {
            animateNumberValue(stat, value);
        }
    });
}

function animateNumberValue(element, finalValue) {
    const numericValue = parseInt(finalValue.replace(/[^0-9]/g, ''));
    let currentValue = 0;
    const increment = Math.ceil(numericValue / 50);
    const timer = setInterval(() => {
        currentValue += increment;
        if (currentValue >= numericValue) {
            element.innerText = finalValue;
            clearInterval(timer);
        } else {
            element.innerText = currentValue;
        }
    }, 20);
}

function animateMoneyValue(element, finalValue) {
    const numericValue = parseFloat(finalValue.replace('R$ ', '').replace('M', '')) * 1000000;
    let currentValue = 0;
    const increment = numericValue / 50;
    const timer = setInterval(() => {
        currentValue += increment;
        if (currentValue >= numericValue) {
            element.innerText = finalValue;
            clearInterval(timer);
        } else {
            if (currentValue >= 1000000) {
                element.innerText = `R$ ${(currentValue / 1000000).toFixed(1)}M`;
            } else {
                element.innerText = `R$ ${Math.round(currentValue / 1000)}K`;
            }
        }
    }, 20);
}

// Tooltip Functions
function showTooltip(event, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'fixed bg-slate-800 text-white text-sm py-1 px-2 rounded-lg pointer-events-none z-50 border border-cyan-500/30';
    tooltip.style.left = event.pageX + 10 + 'px';
    tooltip.style.top = event.pageY - 30 + 'px';
    tooltip.innerText = text;
    
    document.body.appendChild(tooltip);
    
    event.target.addEventListener('mouseleave', function() {
        tooltip.remove();
    });
}

function hideTooltip() {
    const tooltips = document.querySelectorAll('.fixed.bg-slate-800');
    tooltips.forEach(tooltip => tooltip.remove());
}

// Event Listeners
function setupEventListeners() {
    // Fechar sidebar ao clicar no overlay
    const overlay = document.getElementById('sidebar-overlay');
    if (overlay) {
        overlay.addEventListener('click', function() {
            toggleSidebar();
        });
    }
    
    // Atualizar dados em tempo real (simulado)
    setupRealTimeUpdates();
    
    // Responsive adjustments
    handleResize();
    window.addEventListener('resize', handleResize);
}

function setupRealTimeUpdates() {
    // Simular atualizações em tempo real a cada 30 segundos
    setInterval(() => {
        updateStats();
    }, 30000);
}

function updateStats() {
    console.log('Atualizando estatísticas...');
    
    // Adicionar efeito de loading nos cards
    const cards = document.querySelectorAll('.glass.rounded-2xl');
    cards.forEach(card => {
        card.classList.add('pulse-neon');
        
        setTimeout(() => {
            card.classList.remove('pulse-neon');
        }, 2000);
    });
}

function handleResize() {
    // Fechar sidebar automaticamente em telas grandes
    if (window.innerWidth >= 1024) {
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        
        if (sidebar && sidebar.classList.contains('-translate-x-full')) {
            sidebar.classList.remove('-translate-x-full');
        }
        
        if (overlay && !overlay.classList.contains('hidden')) {
            overlay.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
    }
}

// Export functions if using modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        toggleSidebar,
        initializeDashboard
    };
}