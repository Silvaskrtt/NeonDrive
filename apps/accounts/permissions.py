# apps/accounts/permissions.py

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

# Apps do sistema
APPS = ['clients', 'reports', 'dashboard']

def create_groups_and_permissions():
    """
    Cria grupos e permissões para o sistema
    """
    
    # ========================================
    # GRUPOS
    # ========================================
    
    grupo_admin, _ = Group.objects.get_or_create(name='Administradores')
    grupo_vendedor, _ = Group.objects.get_or_create(name='Vendedores')
    grupo_gerente, _ = Group.objects.get_or_create(name='Gerentes')
    
    # ========================================
    # PERMISSÕES BASE
    # ========================================
    
    # Buscar todas as permissões dos apps
    permissoes_clients = Permission.objects.filter(
        Q(content_type__app_label='clients')
    )
    
    permissoes_reports = Permission.objects.filter(
        Q(content_type__app_label='reports')
    )
    
    permissoes_dashboard = Permission.objects.filter(
        Q(content_type__app_label='dashboard')
    )
    
    # ========================================
    # ATRIBUIR PERMISSÕES AOS GRUPOS
    # ========================================
    
    # ADMIN - todas as permissões
    grupo_admin.permissions.set(
        list(permissoes_clients) + 
        list(permissoes_reports) + 
        list(permissoes_dashboard)
    )
    
    # GERENTE - pode ver tudo e editar clientes, mas não relatórios
    permissoes_gerente = []
    
    # Permissões de clientes para gerente (ver e editar)
    for p in permissoes_clients:
        if any(x in p.codename for x in ['view', 'add', 'change']):
            permissoes_gerente.append(p)
    
    # Dashboard (só visualização)
    for p in permissoes_dashboard:
        if 'view' in p.codename:
            permissoes_gerente.append(p)
    
    grupo_gerente.permissions.set(permissoes_gerente)
    
    # VENDEDOR - só visualização básica
    permissoes_vendedor = []
    
    for p in permissoes_clients:
        if 'view' in p.codename:
            permissoes_vendedor.append(p)
    
    for p in permissoes_dashboard:
        if 'view' in p.codename:
            permissoes_vendedor.append(p)
    
    grupo_vendedor.permissions.set(permissoes_vendedor)
    
    print("✅ Grupos e permissões criados com sucesso!")
    print(f"Administradores: {grupo_admin.permissions.count()} permissões")
    print(f"Gerentes: {grupo_gerente.permissions.count()} permissões")
    print(f"Vendedores: {grupo_vendedor.permissions.count()} permissões")