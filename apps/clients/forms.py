# apps/clients/forms.py

from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'cpf', 'email', 'phone', 'address', 'document']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Endereço completo'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nome',
            'cpf': 'CPF',
            'email': 'E-mail',
            'phone': 'Telefone',
            'address': 'Endereço',
            'document': 'Documento',
        }
    
    def clean_cpf(self):
        """Validação adicional do CPF no form"""
        cpf = self.cleaned_data.get('cpf')
        
        # Remove caracteres não numéricos para validação
        cpf_numeros = ''.join(filter(str.isdigit, cpf))
        
        # Verifica se tem 11 dígitos
        if len(cpf_numeros) != 11:
            raise forms.ValidationError('CPF deve ter 11 dígitos')
        
        # Verifica se não é uma sequência repetida
        if cpf_numeros == cpf_numeros[0] * 11:
            raise forms.ValidationError('CPF inválido')
        
        # Validação dos dígitos verificadores
        for i in range(9, 11):
            soma = 0
            for j in range(i):
                soma += int(cpf_numeros[j]) * (i + 1 - j)
            digito = (soma * 10 % 11) % 10
            if digito != int(cpf_numeros[i]):
                raise forms.ValidationError('CPF inválido')
        
        return cpf