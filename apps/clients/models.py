# apps/clients/models.py

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_cpf(value):
    """Validador de CPF"""
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, value))
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos')
    
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido')
    
    # Validação dos dígitos verificadores
    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != int(cpf[i]):
            raise ValidationError('CPF inválido')


class Client(models.Model):
    name = models.CharField('Nome', max_length=100)
    cpf = models.CharField('CPF', max_length=14, unique=True, validators=[validate_cpf])
    email = models.EmailField('E-mail')
    phone = models.CharField('Telefone', max_length=20)
    address = models.TextField('Endereço', blank=True, null=True)
    document = models.FileField('Documento', upload_to='documents/', blank=True, null=True)
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def clean(self):
        """Limpa e formata o CPF antes de salvar"""
        if self.cpf:
            # Remove caracteres não numéricos
            cpf_clean = ''.join(filter(str.isdigit, self.cpf))
            # Formata o CPF (XXX.XXX.XXX-XX)
            if len(cpf_clean) == 11:
                self.cpf = f'{cpf_clean[:3]}.{cpf_clean[3:6]}.{cpf_clean[6:9]}-{cpf_clean[9:]}'
    
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)