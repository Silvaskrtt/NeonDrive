// Inicialização de componentes
document.addEventListener('DOMContentLoaded', function() {
    console.log('AutoNex - Sistema de Vendas inicializado');
    
    // Adicionar classe active ao item do sidebar atual
    const currentPath = window.location.pathname;
    const sidebarItems = document.querySelectorAll('.sidebar-item');
    
    sidebarItems.forEach(item => {
        if (item.getAttribute('href') === currentPath) {
            item.classList.add('active');
        }
    });
});