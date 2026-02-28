# accounts/decorators.py
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps
from .models import Profile

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role == 'ADMIN':
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("Acesso negado. Área restrita para administradores.")
        except Profile.DoesNotExist:
            # Se não tiver perfil, redireciona para criar (embora o signal já crie automaticamente)
            return redirect('profile_create')
    return _wrapped_view

def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role == 'USER':
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("Acesso negado. Área restrita para usuários comuns.")
        except Profile.DoesNotExist:
            return redirect('profile_create')
    return _wrapped_view

def role_required(allowed_roles=[]):
    """Decorator mais flexível que aceita múltiplas roles"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            try:
                if request.user.profile.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden(f"Acesso negado. Roles permitidas: {', '.join(allowed_roles)}")
            except Profile.DoesNotExist:
                return redirect('profile_create')
        return _wrapped_view
    return decorator