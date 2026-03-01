from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from .models import Sale

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    # Campos a serem exibidos na listagem
    list_display = [
        'id', 
        'client', 
        'vehicle', 
        'formatted_value', 
        'payment_method', 
        'status_colored', 
        'sale_date', 
        'user'
    ]
    
    # Campos que serão links para edição
    list_display_links = ['id', 'client']
    
    # Campos que podem ser usados para busca
    search_fields = [
        'client__name', 
        'client__cpf', 
        'vehicle__model', 
        'vehicle__plate',
        'user__username'
    ]
    
    # Filtros laterais
    list_filter = [
        'status', 
        'payment_method', 
        'sale_date',
        'user'
    ]
    
    # Campos para ordenação padrão
    ordering = ['-sale_date']
    
    # Paginação
    list_per_page = 20
    
    # Campos somente leitura
    readonly_fields = ['sale_date', 'formatted_value_display']
    
    # Campos a serem exibidos no formulário de edição/adicionar
    fieldsets = (
        ('Informações da Venda', {
            'fields': (
                'value',
                'payment_method',
                'status',
            )
        }),
        ('Relacionamentos', {
            'fields': (
                'vehicle',
                'client',
                'user',
            )
        }),
        ('Datas', {
            'fields': (
                'sale_date',
            ),
            'classes': ('collapse',),  # Seção recolhível
        }),
    )
    
    # Autocompletar para campos de relacionamento
    autocomplete_fields = ['vehicle', 'client', 'user']
    
    # Ações personalizadas
    actions = ['mark_as_done', 'mark_as_canceled']
    
    def formatted_value(self, obj):
        """Formata o valor da venda em reais"""
        return f'R$ {obj.value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    formatted_value.short_description = 'Valor'
    formatted_value.admin_order_field = 'value'
    
    def formatted_value_display(self, obj):
        """Exibe o valor formatado nos detalhes"""
        return self.formatted_value(obj)
    formatted_value_display.short_description = 'Valor Formatado'
    
    def status_colored(self, obj):
        """Exibe o status com cores diferentes"""
        colors = {
            'Pending': 'orange',
            'Done': 'green',
            'Canceled': 'red',
        }
        status_names = dict(Sale.STATUS_CHOICES)
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            status_names.get(obj.status, obj.status)
        )
    status_colored.short_description = 'Status'
    status_colored.admin_order_field = 'status'
    
    def mark_as_done(self, request, queryset):
        """Ação para marcar vendas como concluídas"""
        updated = queryset.update(status='Done')
        self.message_user(
            request, 
            f'{updated} venda(s) foram marcadas como concluída(s).'
        )
    mark_as_done.short_description = 'Marcar vendas selecionadas como Concluídas'
    
    def mark_as_canceled(self, request, queryset):
        """Ação para marcar vendas como canceladas"""
        updated = queryset.update(status='Canceled')
        self.message_user(
            request, 
            f'{updated} venda(s) foram marcadas como cancelada(s).'
        )
    mark_as_canceled.short_description = 'Marcar vendas selecionadas como Canceladas'
    
    # Sobrescrevendo o método save_model para adicionar lógica personalizada se necessário
    def save_model(self, request, obj, form, change):
        if not obj.user_id:  # Se o usuário não foi definido
            obj.user = request.user  # Define o usuário logado
        super().save_model(request, obj, form, change)
    
    # Estatísticas no topo do changelist
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Calcula algumas estatísticas
        total_vendas = Sale.objects.count()
        valor_total = Sale.objects.filter(status='Done').aggregate(
            total=models.Sum('value')
        )['total'] or 0
        
        extra_context['total_vendas'] = total_vendas
        extra_context['valor_total'] = f'R$ {valor_total:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        
        return super().changelist_view(request, extra_context=extra_context)