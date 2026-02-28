/**
 * Script para melhorias na tabela de vendas
 */
document.addEventListener('DOMContentLoaded', () => {
    // Exemplo: Destacar linhas quando o mouse passar (opcional via JS)
    const rows = document.querySelectorAll('.table-row');
    
    rows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            // Você pode adicionar lógicas de analytics ou efeitos extras aqui
        });
    });
});

// Função utilitária para formatar moeda se precisar via JS
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}