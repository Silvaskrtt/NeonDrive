# apps/sales/forms.py

from django import forms
from django.db import models
from .models import Sale
from clients.models import Client
from vehicles.models import Vehicle

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['value', 'payment_method', 'status', 'vehicle', 'client', 'user']
        widgets = {
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0,00'
            }),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'value': 'Valor Total (R$)',
            'payment_method': 'Método de Pagamento',
            'status': 'Status da Venda',
            'vehicle': 'Veículo',
            'client': 'Cliente',
            'user': 'Usuário Responsável',
        }
        help_texts = {
            'value': 'Digite o valor total da venda',
            'vehicle': 'Selecione o veículo vendido',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtra apenas veículos disponíveis (se tiver esse campo)
        if hasattr(Vehicle, 'status'):
            self.fields['vehicle'].queryset = Vehicle.objects.filter(status='available')
        
        # Filtra apenas clientes ativos (se tiver esse campo)
        if hasattr(Client, 'is_active'):
            self.fields['client'].queryset = Client.objects.filter(is_active=True)
        
        # User não é obrigatório no form (será preenchido automaticamente)
        self.fields['user'].required = False
        
        # Se for edição, mostra o usuário atual
        if self.instance and self.instance.pk:
            self.fields['user'].required = False
            self.fields['user'].widget.attrs['readonly'] = True
    
    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value and value <= 0:
            raise forms.ValidationError('O valor da venda deve ser maior que zero.')
        return value
    
    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get('vehicle')
        client = cleaned_data.get('client')
        
        # Validação personalizada: verificar se o veículo já não foi vendido
        if vehicle and vehicle.sale_set.exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('Este veículo já foi vendido!')
        
        return cleaned_data