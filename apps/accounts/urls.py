from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('password/change/', views.password_change, name='password_change'),
    # Adicione outras URLs conforme necessário
]