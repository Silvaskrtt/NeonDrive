# apps/vehicles/urls.py

from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    path('', views.VehicleList.as_view(), name='list'),
    path('<int:pk>/', views.VehicleDetail.as_view(), name='detail'),
    path('novo/', views.VehicleCreate.as_view(), name='create'),
    path('<int:pk>/editar/', views.VehicleUpdate.as_view(), name='update'),
    path('<int:pk>/deletar/', views.VehicleDelete.as_view(), name='delete'),
    path('<int:pk>/detalhes/', views.VehicleDetailJSON.as_view(), name='detail_json'),
    path('buscar/', views.VehicleSearchJSON.as_view(), name='search_json'),
]