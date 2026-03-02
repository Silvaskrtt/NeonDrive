# apps/sales/urls.py

from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.SaleList.as_view(), name='list'),
    path('nova/', views.SaleCreate.as_view(), name='create'),
    path('<int:pk>/', views.SaleDetail.as_view(), name='detail'),
    path('<int:pk>/editar/', views.SaleUpdate.as_view(), name='update'),
    path('<int:pk>/deletar/', views.SaleDelete.as_view(), name='delete'),
    path('<int:pk>/detalhes/', views.SaleDetailJSON.as_view(), name='detail_json'),
    path('get-vehicle-data/<int:pk>/', views.GetVehicleDataJSON.as_view(), name='get_vehicle_data'),
]