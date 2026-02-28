from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    # Campos que aparecem na lista
    list_display = (
        'mark',
        'model',
        'year',
        'car_plate',
        'color',
        'value',
        'status',
        'user',
        'created_at',
        'image_preview'
    )

    # Filtros laterais
    list_filter = (
        'status',
        'year',
        'color',
        'created_at',
    )

    # Busca no topo
    search_fields = (
        'mark',
        'model',
        'car_plate',
        'color',
        'user__username',
        'user__email',
    )

    # Ordenação padrão
    ordering = (
        '-created_at',
    )

    # Paginação
    list_per_page = 25

    # Campos somente leitura
    readonly_fields = (
        'created_at',
        'image_preview',
    )

    # Organização do formulário
    fieldsets = (
        ('Informações do Veículo', {
            'fields': (
                'mark',
                'model',
                'year',
                'color',
                'car_plate',
            )
        }),

        ('Dados Comerciais', {
            'fields': (
                'value',
                'status',
            )
        }),

        ('Responsável', {
            'fields': (
                'user',
            )
        }),

        ('Registro', {
            'fields': (
                'created_at',
            )
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" style="object-fit: cover;" />'
        return "Sem imagem"
    image_preview.allow_tags = True
    image_preview.short_description = "Pré-visualização"