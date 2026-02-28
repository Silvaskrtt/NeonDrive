# apps/accounts/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

class Profile(models.Model):

    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('USER', 'Usuário'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    def save(self, *args, **kwargs):
        """Ao salvar o perfil, atualiza o grupo do usuário"""
        # Primeiro salva o perfil
        super().save(*args, **kwargs)
        # Depois atualiza o grupo (sem salvar o user)
        self.update_user_group()
        
    def update_user_group(self):
        """Atualiza o grupo do usuário baseado na role"""
        from django.contrib.auth.models import Group
        
        # Determina qual grupo deve ter baseado na role
        grupo_destino = None
        if self.role == 'ADMIN':
            grupo_destino = 'Administradores'
        elif self.role == 'USER':
            grupo_destino = 'Vendedores'
        
        if grupo_destino:
            try:
                # Remove de todos os grupos primeiro
                self.user.groups.clear()
                # Adiciona ao grupo correto
                grupo = Group.objects.get(name=grupo_destino)
                self.user.groups.add(grupo)
            except Group.DoesNotExist:
                pass


# Signal para criar perfil automaticamente
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Cria um perfil automaticamente quando um usuário é criado"""
    if created:
        Profile.objects.create(user=instance)


# Signal para salvar perfil
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Salva o perfil quando o usuário é salvo"""
    if not kwargs.get('created', False):  # Só executa se NÃO for criação
        try:
            if hasattr(instance, 'profile'):
                # Só salva se a role não mudou recentemente
                pass  # Não faz nada para evitar loop
        except:
            pass