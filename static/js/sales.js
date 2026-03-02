// static/js/sales.js

// Função para visualizar venda no modal
function viewSale(saleId) {
    const modal = document.getElementById('saleModal');
    const modalContent = document.getElementById('modalContent');
    
    if (!modal || !modalContent) return;
    
    // Mostra modal com loading
    modal.classList.remove('hidden');
    modalContent.innerHTML = `
        <div class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-400"></div>
        </div>
    `;
    
    // Busca dados da venda
    fetch(`/vendas/${saleId}/detalhes/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                modalContent.innerHTML = `
                    <div class="text-center py-8">
                        <p class="text-red-400">${data.error}</p>
                    </div>
                `;
            } else {
                modalContent.innerHTML = `
                    <div class="space-y-4">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <p class="text-sm text-slate-500">ID da Venda</p>
                                <p class="text-white font-mono">#${data.id.toString().padStart(4, '0')}</p>
                            </div>
                            <div>
                                <p class="text-sm text-slate-500">Data</p>
                                <p class="text-white">${data.sale_date}</p>
                            </div>
                        </div>
                        
                        <div class="border-t border-slate-700 pt-4">
                            <p class="text-sm text-slate-500 mb-2">Cliente</p>
                            ${data.client ? `
                                <p class="text-white font-medium">${data.client.name}</p>
                                <p class="text-sm text-slate-400">${data.client.email}</p>
                                <p class="text-sm text-slate-400">${data.client.phone}</p>
                            ` : '<p class="text-slate-400">N/A</p>'}
                        </div>
                        
                        <div class="border-t border-slate-700 pt-4">
                            <p class="text-sm text-slate-500 mb-2">Veículo</p>
                            ${data.vehicle ? `
                                <p class="text-white font-medium">${data.vehicle.model}</p>
                                <p class="text-sm text-slate-400">Placa: ${data.vehicle.plate}</p>
                                <p class="text-sm text-slate-400">Ano: ${data.vehicle.year}</p>
                            ` : '<p class="text-slate-400">N/A</p>'}
                        </div>
                        
                        <div class="border-t border-slate-700 pt-4">
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <p class="text-sm text-slate-500">Valor</p>
                                    <p class="text-cyan-400 font-bold text-xl">R$ ${parseFloat(data.value).toFixed(2).replace('.', ',')}</p>
                                </div>
                                <div>
                                    <p class="text-sm text-slate-500">Método</p>
                                    <p class="text-white">${data.payment_method}</p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="border-t border-slate-700 pt-4">
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <p class="text-sm text-slate-500">Status</p>
                                    <span class="px-3 py-1 rounded-full text-xs font-medium inline-block mt-1
                                        ${data.status === 'Concluída' ? 'bg-green-500/20 text-green-400 border border-green-500/50' : 
                                          data.status === 'Pendente' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/50' : 
                                          'bg-red-500/20 text-red-400 border border-red-500/50'}">
                                        ${data.status}
                                    </span>
                                </div>
                                <div>
                                    <p class="text-sm text-slate-500">Vendedor</p>
                                    <p class="text-white">${data.user}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }
        })
        .catch(error => {
            modalContent.innerHTML = `
                <div class="text-center py-8">
                    <p class="text-red-400">Erro ao carregar dados da venda</p>
                </div>
            `;
            console.error('Error:', error);
        });
}

// Função para fechar modal
function closeModal() {
    const modal = document.getElementById('saleModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

// Fecha modal com tecla ESC
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});

// Confirmação antes de deletar (caso não use a página de confirmação)
function confirmDelete(saleId) {
    if (confirm('Tem certeza que deseja excluir esta venda?')) {
        window.location.href = `/vendas/${saleId}/deletar/`;
    }
}