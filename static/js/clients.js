/**
 * Gerenciamento da página de Clientes
 */

// Abre o modal de cadastro/edição
function openClientModal() {
    const modal = document.getElementById('client-modal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

// Fecha o modal
function closeClientModal() {
    const modal = document.getElementById('client-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

// Exibe feedback de sucesso temporário
function showSuccessFeedback() {
    const feedback = document.getElementById('feedback-success');
    feedback.classList.remove('hidden');
    
    // Esconde após 4 segundos
    setTimeout(() => {
        feedback.classList.add('hidden');
    }, 4000);
}

// Filtro de busca simples (Front-end)
document.querySelector('input[placeholder="Buscar cliente..."]').addEventListener('input', function(e) {
    const term = e.target.value.toLowerCase();
    const rows = document.querySelectorAll('.table-row');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
    });
});