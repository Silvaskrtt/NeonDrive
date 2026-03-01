from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from clients.models import Client
from vehicles.models import Vehicle
from sales.models import Sale
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

@login_required
def home(request):
    # Dados para os cards
    total_clients = Client.objects.count()
    total_vehicles = Vehicle.objects.count()
    total_sales = Sale.objects.count()
    
    # Vendas do mês atual
    month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0)
    monthly_sales = Sale.objects.filter(sale_date__gte=month_start)
    monthly_sales_count = monthly_sales.count()
    
    # Receita total
    total_revenue = Sale.objects.aggregate(total=Sum('value'))['total'] or 0
    
    # Vendas por mês para o gráfico
    last_6_months = []
    for i in range(5, -1, -1):
        month = timezone.now() - timedelta(days=30 * i)
        month_sales = Sale.objects.filter(
            sale_date__year=month.year,
            sale_date__month=month.month
        ).count()
        last_6_months.append({
            'month': month.strftime('%b'),
            'count': month_sales
        })
    
    # Veículos por status para o gráfico de categorias
    vehicles_by_status = {
        'available': Vehicle.objects.filter(status='available').count(),
        'reserved': Vehicle.objects.filter(status='reserved').count(),
        'sold': Vehicle.objects.filter(status='sold').count(),
    }
    
    # Vendas recentes
    recent_sales = Sale.objects.select_related('client', 'vehicle').order_by('-sale_date')[:5]
    
    context = {
        'total_clients': total_clients,
        'total_vehicles': total_vehicles,
        'total_sales': total_sales,
        'monthly_sales': monthly_sales_count,
        'total_revenue': total_revenue,
        'monthly_chart_data': last_6_months,
        'vehicles_by_status': vehicles_by_status,
        'recent_sales': recent_sales,
    }
    
    return render(request, 'dashboard/home.html', context)