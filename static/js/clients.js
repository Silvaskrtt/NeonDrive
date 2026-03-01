/**
 * Gerenciamento da página de Clientes
 */

// Variável global para controlar o ID do cliente em edição
let currentEditingClientId = null;

// Abre o modal de cadastro/edição
function openClientModal(clientId = null) {
    const modal = document.getElementById('client-modal');
    const modalTitle = document.getElementById('modal-title');
    const form = document.getElementById('client-form');
    
    if (!modal) return;
    
    // Reset do formulário
    form.reset();
    document.getElementById('client-id').value = '';
    document.getElementById('current-document-preview').classList.add('hidden');
    
    if (clientId) {
        // Modo edição
        modalTitle.textContent = 'Editar Cliente';
        currentEditingClientId = clientId;
        loadClientData(clientId);
    } else {
        // Modo criação
        modalTitle.textContent = 'Novo Cliente';
        currentEditingClientId = null;
    }
    
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

// Carrega dados do cliente para edição
function loadClientData(clientId) {
    fetch(`/clientes/${clientId}/detalhes/`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('name').value = data.name || '';
        document.getElementById('cpf').value = data.cpf || '';
        document.getElementById('email').value = data.email || '';
        document.getElementById('phone').value = data.phone || '';
        document.getElementById('address').value = data.address || '';
        
        if (data.document) {
            const preview = document.getElementById('current-document-preview');
            const docLink = document.getElementById('document-link');
            docLink.href = data.document;
            preview.classList.remove('hidden');
        }
    })
    .catch(error => {
        console.error('Erro ao carregar cliente:', error);
        showFeedback('Erro ao carregar dados do cliente', 'error');
    });
}

// Fecha o modal
function closeClientModal() {
    const modal = document.getElementById('client-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
        currentEditingClientId = null;
    }
}

// Exibe feedback
function showFeedback(message, type = 'success') {
    const feedback = document.getElementById('feedback-success');
    if (!feedback) return;
    
    const messageEl = feedback.querySelector('p');
    messageEl.textContent = message;
    
    if (type === 'success') {
        messageEl.className = 'font-medium text-green-400';
    } else {
        messageEl.className = 'font-medium text-red-400';
    }
    
    feedback.classList.remove('hidden');
    
    setTimeout(() => {
        feedback.classList.add('hidden');
    }, 4000);
}

// Submete o formulário via método tradicional (não AJAX)
function submitClientForm(event) {
    event.preventDefault();
    
    const form = event.target;
    
    // Se for edição, muda a action do form para a URL de edição
    if (currentEditingClientId) {
        form.action = `/clientes/${currentEditingClientId}/editar/`;
    } else {
        form.action = '/clientes/novo/';
    }
    
    // Submete o formulário normalmente (recarrega a página)
    form.submit();
}

// Visualizar cliente
function viewClient(clientId) {
    window.location.href = `/clientes/${clientId}/`;
}

// Editar cliente
function editClient(clientId) {
    openClientModal(clientId);
}

// Excluir cliente
function deleteClient(clientId) {
    if (confirm('Tem certeza que deseja excluir este cliente?')) {
        // Usa o formulário de exclusão normal (recarrega a página)
        window.location.href = `/clientes/${clientId}/deletar/`;
    }
}

// Inicializa quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log('Clientes JS inicializado');
    
    // Configurar o formulário do modal
    const form = document.getElementById('client-form');
    if (form) {
        form.addEventListener('submit', submitClientForm);
    }
    
    // Filtro de busca
    const searchInput = document.querySelector('input[placeholder="Buscar cliente..."]');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const term = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('.table-row');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(term) ? '' : 'none';
            });
        });
    }
    
    // Máscara para CPF
    const cpfInput = document.getElementById('cpf');
    if (cpfInput) {
        cpfInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) value = value.slice(0, 11);
            
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            
            e.target.value = value;
        });
    }
    
    // Máscara para telefone
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) value = value.slice(0, 11);
            
            if (value.length <= 10) {
                value = value.replace(/(\d{2})(\d)/, '($1) $2');
                value = value.replace(/(\d{4})(\d)/, '$1-$2');
            } else {
                value = value.replace(/(\d{2})(\d)/, '($1) $2');
                value = value.replace(/(\d{5})(\d)/, '$1-$2');
            }
            
            e.target.value = value;
        });
    }
});