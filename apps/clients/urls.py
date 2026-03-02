# apps/clients/urls.py

from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.ClientList.as_view(), name='list'),
    path('<int:pk>/', views.ClientDetail.as_view(), name='detail'),
    path('novo/', views.ClientCreate.as_view(), name='create'),
    path('<int:pk>/editar/', views.ClientUpdate.as_view(), name='update'),
    path('<int:pk>/deletar/', views.ClientDelete.as_view(), name='delete'),
    path('<int:pk>/detalhes/', views.ClientDetailJSON.as_view(), name='detail_json'),
    path('<int:pk>/toggle-status/', views.ClientToggleStatus.as_view(), name='toggle_status'),
]