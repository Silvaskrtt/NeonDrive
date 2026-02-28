/**
 * Gerenciamento da Vitrine de Veículos
 */
document.addEventListener('DOMContentLoaded', () => {
    const vehicleCards = document.querySelectorAll('.vehicle-card');

    vehicleCards.forEach(card => {
        card.addEventListener('click', (e) => {
            // Evita disparar o clique do card se clicar no botão de editar
            if (e.target.closest('.action-btn-circle')) return;
            
            const model = card.querySelector('h4').innerText;
            console.log(`Abrindo detalhes de: ${model}`);
            // Aqui você poderia redirecionar: window.location.href = `/veiculos/detalhes/${id}`;
        });
    });
});

// Função para abrir o formulário de novo veículo
function openVehicleModal() {
    // Lógica similar ao modal de clientes
    console.log("Abrindo modal de veículos...");
}