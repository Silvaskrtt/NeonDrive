document.addEventListener('DOMContentLoaded', () => {

    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('mobile-menu-btn');

    if (!sidebar || !toggleBtn) {
        console.warn('Sidebar ou botão não encontrado');
        return;
    }

    // Abrir / fechar
    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('-translate-x-full');
    });

    // Fechar ao clicar nos links
    document.querySelectorAll('.sidebar-item').forEach(item => {
        item.addEventListener('click', () => {

            if (window.innerWidth < 1024) {
                sidebar.classList.add('-translate-x-full');
            }

        });
    });

});