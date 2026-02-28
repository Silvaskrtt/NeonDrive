/**
 * Alterna a visibilidade da Sidebar.
 * Note que o botão no HTML chama onclick="toggleSidebar()", 
 * então definimos ela no escopo global.
 */
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('-translate-x-full');
    } else {
        console.warn("Elemento #sidebar não encontrado.");
    }
}

// Opcional: Fechar ao clicar fora do menu no mobile
document.addEventListener('click', (e) => {
    const sidebar = document.getElementById('sidebar');
    const menuBtn = document.getElementById('mobile-menu-btn');
    
    if (window.innerWidth < 1024 && 
        sidebar && 
        !sidebar.contains(e.target) && 
        !menuBtn.contains(e.target) &&
        !sidebar.classList.contains('-translate-x-full')) {
        
        sidebar.classList.add('-translate-x-full');
    }
});