from django.db import models
import os

def vehicle_image_path(instance, filename):
    """Gera um caminho único para cada imagem de veículo"""
    ext = filename.split('.')[-1]
    filename = f"{instance.mark}_{instance.model}_{instance.car_plate}.{ext}"
    return os.path.join('vehicles', filename)

class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('available', 'Disponível'),
        ('reserved', 'Reservado'),
        ('sold', 'Vendido'),
    ]
    
    mark = models.CharField(max_length=50, verbose_name="Marca")
    model = models.CharField(max_length=50, verbose_name="Modelo")
    year = models.PositiveIntegerField(verbose_name="Ano")
    car_plate = models.CharField(max_length=10, unique=True, verbose_name="Placa")
    color = models.CharField(max_length=20, verbose_name="Cor")
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    
    # Campo de imagem
    image = models.ImageField(
        upload_to=vehicle_image_path, 
        verbose_name="Imagem do Veículo",
        null=True, 
        blank=True
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='available',
        verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Usuário")
    
    def __str__(self):
        return f"{self.mark} {self.model} - {self.car_plate}"

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ['-created_at']