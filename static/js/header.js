/**
 * Header JavaScript simplificado
 */
document.addEventListener('DOMContentLoaded', function() {
    initProfileMenu();
});

/**
 * Inicializa o menu dropdown do perfil
 */
function initProfileMenu() {
    const profileBtn = document.getElementById('profile-menu-btn');
    const dropdown = document.getElementById('profile-dropdown');
    
    if (!profileBtn || !dropdown) return;
    
    // Toggle dropdown ao clicar no perfil
    profileBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        dropdown.classList.toggle('hidden');
    });
    
    // Fechar dropdown ao clicar fora
    document.addEventListener('click', function(e) {
        if (!profileBtn.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.add('hidden');
        }
    });
    
    // Impedir que o dropdown feche ao clicar dentro dele
    dropdown.addEventListener('click', function(e) {
        e.stopPropagation();
    });
}

// Função toggleSidebar já existente
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('-translate-x-full');
    }
}

// Fechar sidebar ao clicar fora no mobile
document.addEventListener('click', (e) => {
    const sidebar = document.getElementById('sidebar');
    const menuBtn = document.getElementById('mobile-menu-btn');
    
    if (window.innerWidth < 1024 && 
        sidebar && 
        !sidebar.contains(e.target) && 
        menuBtn && !menuBtn.contains(e.target) &&
        !sidebar.classList.contains('-translate-x-full')) {
        
        sidebar.classList.add('-translate-x-full');
    }
});