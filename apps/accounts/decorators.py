# accounts/decorators.py

from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from .models import Profile

def admin_required(view_func):
    """Apenas administradores podem acessar"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Faça login para continuar.')
            return redirect('account_login')
        
        try:
            if request.user.profile.role == 'ADMIN':
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Acesso negado. Área restrita para administradores.')
                return redirect('dashboard:home')
        except Profile.DoesNotExist:
            messages.error(request, 'Perfil não encontrado. Contate o administrador.')
            return redirect('dashboard:home')
    return _wrapped_view

def user_required(view_func):
    """Apenas usuários comuns podem acessar"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Faça login para continuar.')
            return redirect('account_login')
        
        try:
            if request.user.profile.role == 'USER':
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Acesso negado. Área restrita para usuários comuns.')
                return redirect('dashboard:home')
        except Profile.DoesNotExist:
            messages.error(request, 'Perfil não encontrado. Contate o administrador.')
            return redirect('dashboard:home')
    return _wrapped_view

def role_required(allowed_roles=[]):
    """Aceita múltiplas roles (ex: ['ADMIN', 'USER'])"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Faça login para continuar.')
                return redirect('account_login')
            
            try:
                if request.user.profile.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(
                        request, 
                        f'Acesso negado. Seu perfil não tem permissão para acessar esta página.'
                    )
                    return redirect('dashboard:home')
            except Profile.DoesNotExist:
                messages.error(request, 'Perfil não encontrado. Contate o administrador.')
                return redirect('dashboard:home')
        return _wrapped_view
    return decorator

def group_required(*group_names):
    """Verifica se o usuário pertence a um dos grupos especificados"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Faça login para continuar.')
                return redirect('account_login')
            
            # Superuser tem acesso a tudo
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Verifica se está em algum dos grupos
            if request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            
            messages.error(request, 'Acesso negado. Você não pertence ao grupo necessário.')
            return redirect('dashboard:home')
        return _wrapped_view
    return decorator

def permission_required(perm):
    """Verifica se o usuário tem uma permissão específica"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Faça login para continuar.')
                return redirect('account_login')
            
            if request.user.has_perm(perm):
                return view_func(request, *args, **kwargs)
            
            messages.error(request, f'Acesso negado. Permissão necessária: {perm}')
            return redirect('dashboard:home')
        return _wrapped_view
    return decorator

def any_permission_required(perm_list):
    """Verifica se o usuário tem pelo menos uma das permissões"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Faça login para continuar.')
                return redirect('account_login')
            
            for perm in perm_list:
                if request.user.has_perm(perm):
                    return view_func(request, *args, **kwargs)
            
            messages.error(request, 'Acesso negado. Você não tem as permissões necessárias.')
            return redirect('dashboard:home')
        return _wrapped_view
    return decorator

# DECORATOR COMBINADO (ROLE + GRUPO)

def access_required(allowed_roles=[], allowed_groups=[]):
    """Combina verificação de roles e grupos"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Faça login para continuar.')
                return redirect('account_login')
            
            # Superuser tem acesso
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            acesso_permitido = False
            
            # Verifica roles
            try:
                if request.user.profile.role in allowed_roles:
                    acesso_permitido = True
            except:
                pass
            
            # Verifica grupos
            if request.user.groups.filter(name__in=allowed_groups).exists():
                acesso_permitido = True
            
            if acesso_permitido:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, 'Acesso negado. Você não tem permissão para acessar esta página.')
            return redirect('dashboard:home')
        return _wrapped_view
    return decorator