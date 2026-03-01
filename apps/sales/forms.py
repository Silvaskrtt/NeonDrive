# apps/sales/forms.py
from django.db import models
from django import forms
from .models import Sale
from clients.models import Client
from vehicles.models import Vehicle

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['value', 'payment_method', 'status', 'vehicle', 'client']
        widgets = {
            'value': forms.NumberInput(attrs={
                'class': 'form-control w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-cyan-500 transition-colors',
                'step': '0.01',
                'min': '0',
                'placeholder': '0,00'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-control w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-cyan-500 transition-colors'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-cyan-500 transition-colors'
            }),
            'vehicle': forms.Select(attrs={
                'class': 'form-control w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-cyan-500 transition-colors'
            }),
            'client': forms.Select(attrs={
                'class': 'form-control w-full px-4 py-3 bg-slate-800/50 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-cyan-500 transition-colors'
            }),
        }
        labels = {
            'value': 'Valor Total (R$)',
            'payment_method': 'Método de Pagamento',
            'status': 'Status da Venda',
            'vehicle': 'Veículo',
            'client': 'Cliente',
        }
        help_texts = {
            'value': 'Digite o valor total da venda',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtra veículos disponíveis
        self.fields['vehicle'].queryset = Vehicle.objects.filter(status='available')
        
        self.fields['client'].queryset = Client.objects.all()
        
        # Adiciona classes CSS adicionais
        self.fields['value'].widget.attrs['class'] += ' text-right'
        
        # Se for edição, permite veículos já vendidos (o veículo atual)
        if self.instance and self.instance.pk:
            vehicle = self.instance.vehicle
            if vehicle and vehicle.status != 'available':
                self.fields['vehicle'].queryset = Vehicle.objects.filter(
                    models.Q(status='available') | models.Q(pk=vehicle.pk)
                )
    
    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value and value <= 0:
            raise forms.ValidationError('O valor da venda deve ser maior que zero.')
        return value
    
    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get('vehicle')
        
        # Validação: verificar se o veículo já não foi vendido
        if vehicle and vehicle.pk:
            # Exclui a venda atual da verificação (para edição)
            existing_sales = Sale.objects.filter(vehicle=vehicle)
            if self.instance and self.instance.pk:
                existing_sales = existing_sales.exclude(pk=self.instance.pk)
            
            if existing_sales.exists():
                raise forms.ValidationError('Este veículo já foi vendido!')
        
        return cleaned_data