# apps/accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('avatar/upload/', views.avatar_upload, name='avatar_upload'),
    path('password/change/', views.password_change, name='password_change'),
]