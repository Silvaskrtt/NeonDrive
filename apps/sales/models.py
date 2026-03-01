from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.shortcuts import redirect

from clients.models import Client
from vehicles.models import Vehicle

class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('Credit_Card', 'Cartão de Crédito'),
        ('Debit_Card', 'Cartão de Débito'),
        ('Bank_Slip', 'Boleto Bancário'),
        ('Pix', 'Pix'),
        ('Cash', 'Dinheiro em Espécie'),
    ]
    
    STATUS_CHOICES = [
            ('Pending', 'Pendente'),
            ('Done', 'Concluída'),
            ('Canceled', 'Cancelada'),
        ]
    
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Valor Total")
    
    payment_method = models.CharField(
        max_length=50, 
        choices=PAYMENT_CHOICES
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending',
        verbose_name="Status da Venda",
    )
    
    sale_date = models.DateTimeField(_("Data da Venda"), auto_now_add=True)
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Usuário")
    