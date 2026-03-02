from django.urls import path
from . import views
from .views import ExportReportView
from .views import exportar_direto

app_name = 'reports'

urlpatterns = [
    # Página principal
    path('', views.ReportsView.as_view(), name='list'),
    
    # API endpoints
    path('api/dados/', views.ReportsAPIView.as_view(), name='api_dados'),
    path('api/exportar/', views.ExportReportView.as_view(), name='api_exportar'),
    path('api/salvos/', views.SavedReportsView.as_view(), name='api_salvos'),
    path('api/salvos/<int:pk>/', views.SavedReportsView.as_view(), name='api_salvo_detail'),
]