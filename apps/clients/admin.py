# apps/clients/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Administração do modelo Client
    """
    # Campos a serem exibidos na listagem
    list_display = [
        'name', 
        'cpf_formatado', 
        'email', 
        'phone', 
        'created_at', 
        'updated_at',
        'tem_documento'
    ]
    
    # Campos que serão links para a edição
    list_display_links = ['name', 'cpf_formatado']
    
    # Campos para busca
    search_fields = ['name', 'cpf', 'email', 'phone']
    
    # Filtros laterais
    list_filter = ['created_at', 'updated_at']
    
    # Ordenação padrão
    ordering = ['name']
    
    # Paginação
    list_per_page = 25
    
    # Campos que podem ser editados diretamente na listagem
    list_editable = ['email', 'phone']
    
    # Campos somente leitura
    readonly_fields = ['created_at', 'updated_at', 'cpf_formatado_detalhe']
    
    # Organização dos campos no formulário de edição
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('name', 'cpf', 'email', 'phone')
        }),
        ('Endereço e Documentos', {
            'fields': ('address', 'document'),
            'classes': ('wide',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Seção recolhível
        }),
    )
    
    # Métodos personalizados para exibição
    
    def cpf_formatado(self, obj):
        """
        Retorna o CPF formatado para exibição
        """
        if obj.cpf and len(obj.cpf) == 14:  # CPF já formatado
            return obj.cpf
        elif obj.cpf:
            # Formata caso não esteja formatado
            cpf = obj.cpf.replace('.', '').replace('-', '').replace('/', '')
            if len(cpf) == 11:
                return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        return obj.cpf
    
    cpf_formatado.short_description = 'CPF'
    cpf_formatado.admin_order_field = 'cpf'  # Permite ordenar pelo CPF
    
    def cpf_formatado_detalhe(self, obj):
        """
        Versão em destaque do CPF para detalhes
        """
        cpf = self.cpf_formatado(obj)
        return format_html('<strong>{}</strong>', cpf)
    
    cpf_formatado_detalhe.short_description = 'CPF'
    
    def tem_documento(self, obj):
        """
        Indica se o cliente tem documento anexado
        """
        if obj.document:
            return format_html(
                '<img src="/static/admin/img/icon-yes.svg" alt="Sim"> '
                '<a href="{}" target="_blank">Ver</a>',
                obj.document.url
            )
        return format_html('<img src="/static/admin/img/icon-no.svg" alt="Não">')
    
    tem_documento.short_description = 'Documento'
    tem_documento.boolean = False  # Não usa ícone padrão do admin
    
    # Ações personalizadas
    actions = ['exportar_selecionados']
    
    def exportar_selecionados(self, request, queryset):
        """
        Ação para exportar dados dos clientes selecionados
        """
        count = queryset.count()
        self.message_user(
            request, 
            f'{count} cliente(s) selecionado(s) para exportação. '
            f'Implemente a lógica de exportação aqui.'
        )
    
    exportar_selecionados.short_description = "Exportar clientes selecionados"
    
    # Sobrescrevendo métodos para adicionar funcionalidades
    
    def save_model(self, request, obj, form, change):
        """
        Mensagem personalizada ao salvar
        """
        if change:
            mensagem = f'Cliente "{obj.name}" atualizado com sucesso!'
        else:
            mensagem = f'Cliente "{obj.name}" criado com sucesso!'
        
        super().save_model(request, obj, form, change)
        
        # Log da ação
        print(f'{request.user} - {mensagem}')
    
    def delete_model(self, request, obj):
        """
        Mensagem personalizada ao deletar
        """
        nome = obj.name
        super().delete_model(request, obj)
        self.message_user(
            request, 
            f'Cliente "{nome}" removido com sucesso!',
            level='WARNING'
        )
    
    # Personalização do template
    class Media:
        """
        CSS e JS extras para o admin
        """
        css = {
            'all': ('css/admin_custom.css',)
        }
        js = ('js/admin_custom.js',)