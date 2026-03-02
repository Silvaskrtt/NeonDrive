from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
from .forms import UserProfileForm, UserForm

@login_required
def profile_view(request):
    """View do perfil do usuário"""
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        # Se não existir perfil, cria um (fallback)
        profile = Profile.objects.create(user=user)
    
    user_form = UserForm(instance=user)
    profile_form = UserProfileForm(instance=profile)
    password_form = PasswordChangeForm(user)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'account/profile.html', context)

@login_required
def profile_update(request):
    """Atualiza os dados do perfil"""
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Erro ao atualizar perfil. Verifique os dados.')
    
    return redirect('accounts:profile')

@login_required
def password_change(request):
    """Altera a senha do usuário"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Mantém o usuário logado após trocar a senha
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Erro ao alterar senha. Verifique os dados.')
    
    return redirect('accounts:profile')