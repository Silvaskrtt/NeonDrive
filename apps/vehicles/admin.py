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