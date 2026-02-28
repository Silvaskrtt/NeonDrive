# accounts/context_processors.py
def user_profile(request):
    """Disponibiliza informações do perfil do usuário em todas as templates"""
    context = {
        'user_role': None,
        'is_admin': False,
        'is_user': False,
        'has_profile': False
    }
    
    if request.user.is_authenticated:
        try:
            role = request.user.profile.role
            context.update({
                'user_role': role,
                'is_admin': role == 'ADMIN',
                'is_user': role == 'USER',
                'has_profile': True
            })
        except:
            # Usuário autenticado mas sem perfil (improvável devido ao signal)
            pass
    
    return context