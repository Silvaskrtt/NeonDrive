# apps/reports/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SavedReport(models.Model):
    """Modelo para salvar relatórios personalizados"""
    REPORT_TYPES = [
        ('sales', 'Vendas'),
        ('clients', 'Clientes'),
        ('vehicles', 'Veículos'),
        ('performance', 'Performance'),
    ]
    
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]
    
    name = models.CharField('Nome do Relatório', max_length=100)
    report_type = models.CharField('Tipo', max_length=20, choices=REPORT_TYPES)
    format = models.CharField('Formato', max_length=10, choices=FORMAT_CHOICES)
    parameters = models.JSONField('Parâmetros', default=dict)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    file = models.FileField('Arquivo', upload_to='reports/', null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Relatório Salvo'
        verbose_name_plural = 'Relatórios Salvos'
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%d/%m/%Y')}"