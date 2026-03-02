from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from clients.models import Client
from vehicles.models import Vehicle
from sales.models import Sale
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
import calendar

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
    
    # 🔥 CORREÇÃO: Vendas por mês para o gráfico
    # Pegar os últimos 6 meses com dados reais
    last_6_months = []
    
    for i in range(5, -1, -1):
        # Calcula a data do mês
        current_date = timezone.now() - timedelta(days=30 * i)
        
        # Filtra vendas do mês específico
        month_sales_count = Sale.objects.filter(
            sale_date__year=current_date.year,
            sale_date__month=current_date.month
        ).count()
        
        # Calcula o valor total de vendas do mês (se precisar)
        month_sales_value = Sale.objects.filter(
            sale_date__year=current_date.year,
            sale_date__month=current_date.month
        ).aggregate(total=Sum('value'))['total'] or 0
        
        last_6_months.append({
            'month': current_date.strftime('%b'),  # Abreviação do mês
            'full_month': current_date.strftime('%B'),  # Nome completo do mês
            'year': current_date.year,
            'count': month_sales_count,  # Número de vendas
            'value': float(month_sales_value),  # Valor total das vendas
            'month_num': current_date.month  # Número do mês para ordenação
        })
    
    # 🔥 DEBUG: Imprimir no console para verificar
    print(f"Dados do gráfico: {last_6_months}")
    
    # Veículos por status para o gráfico de categorias
    vehicles_by_status = {
        'available': Vehicle.objects.filter(status='available').count(),
        'reserved': Vehicle.objects.filter(status='reserved').count(),
        'sold': Vehicle.objects.filter(status='sold').count(),
    }
    
    # Total de veículos para as porcentagens
    total_vehicles_count = sum(vehicles_by_status.values())
    
    # Vendas recentes
    recent_sales = Sale.objects.select_related('client', 'vehicle').order_by('-sale_date')[:5]
    
    context = {
        'total_clients': total_clients,
        'total_vehicles': total_vehicles,
        'total_sales': total_sales,
        'monthly_sales': monthly_sales_count,
        'total_revenue': total_revenue,
        'monthly_chart_data': last_6_months,  # Dados corrigidos
        'vehicles_by_status': vehicles_by_status,
        'total_vehicles': total_vehicles_count,  # Adicionado para o widthratio
        'recent_sales': recent_sales,
    }
    
    return render(request, 'dashboard/home.html', context)