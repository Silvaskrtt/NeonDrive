# apps/reports/services.py
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta, datetime
from sales.models import Sale
from clients.models import Client
from vehicles.models import Vehicle
import calendar
from decimal import Decimal

class ReportService:
    """Serviço principal para geração de relatórios"""
    
    @staticmethod
    def get_date_range(period):
        """Retorna data de início baseado no período"""
        today = timezone.now()
        
        if period == 'month':
            start_date = today.replace(day=1, hour=0, minute=0, second=0)
        elif period == '3months':
            start_date = (today - timedelta(days=90)).replace(hour=0, minute=0, second=0)
        elif period == 'year':
            start_date = today.replace(month=1, day=1, hour=0, minute=0, second=0)
        else:  # default para mês
            start_date = today.replace(day=1, hour=0, minute=0, second=0)
        
        return start_date
    
    @staticmethod
    def get_vendas_por_marca(period='month'):
        """Relatório de vendas agrupadas por marca"""
        start_date = ReportService.get_date_range(period)
        
        vendas = Sale.objects.filter(
            sale_date__gte=start_date,
            status='Done'
        ).values(
            'vehicle__mark'
        ).annotate(
            total_vendas=Count('id'),
            valor_total=Sum('value')
        ).order_by('-total_vendas')[:4]
        
        # Cores para cada marca
        colors = ['#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899']
        
        result = []
        for i, venda in enumerate(vendas):
            result.append({
                'marca': venda['vehicle__mark'] or 'Não definida',
                'vendas': venda['total_vendas'],
                'valor': float(venda['valor_total'] or 0),
                'color': colors[i % len(colors)]
            })
        
        return result
    
    @staticmethod
    def get_performance_vendedores(period='month'):
        """Relatório de performance dos vendedores"""
        start_date = ReportService.get_date_range(period)
        
        # Vendas por vendedor
        vendas = Sale.objects.filter(
            sale_date__gte=start_date,
            status='Done'
        ).values(
            'user__first_name', 
            'user__last_name',
            'user__username'
        ).annotate(
            total_vendas=Count('id'),
            valor_total=Sum('value'),
            ticket_medio=Avg('value')
        ).order_by('-valor_total')[:3]
        
        result = []
        for venda in vendas:
            nome = venda['user__first_name'] or venda['user__username']
            if venda['user__last_name']:
                nome += f" {venda['user__last_name']}"
            
            result.append({
                'nome': nome,
                'valor': float(venda['valor_total'] or 0),
                'quantidade': venda['total_vendas'],
                'ticket_medio': float(venda.get('ticket_medio', 0) or 0)
            })
        
        return result
    
    @staticmethod
    def get_metricas_gerais(period='month'):
        """Métricas gerais do sistema"""
        start_date = ReportService.get_date_range(period)
        
        # Vendas do período
        vendas = Sale.objects.filter(
            sale_date__gte=start_date,
            status='Done'
        )
        
        # Total de clientes
        total_clientes = Client.objects.count()
        
        # Total de veículos disponíveis
        veiculos_disponiveis = Vehicle.objects.filter(status='available').count()
        
        # Cálculo das métricas
        total_vendas = vendas.count()
        valor_total = vendas.aggregate(total=Sum('value'))['total'] or 0
        
        # Ticket médio
        ticket_medio = valor_total / total_vendas if total_vendas > 0 else 0
        
        # Taxa de conversão (vendas / leads)
        # Considerando que leads são clientes cadastrados no período
        leads_periodo = Client.objects.filter(created_at__gte=start_date).count()
        taxa_conversao = (total_vendas / leads_periodo * 100) if leads_periodo > 0 else 0
        
        return {
            'ticket_medio': float(ticket_medio),
            'taxa_conversao': round(taxa_conversao, 1),
            'leads_mes': leads_periodo,
            'total_vendas': total_vendas,
            'valor_total': float(valor_total),
            'total_clientes': total_clientes,
            'veiculos_disponiveis': veiculos_disponiveis
        }
    
    @staticmethod
    def get_relatorio_detalhado(period='month'):
        """Relatório detalhado por período"""
        start_date = ReportService.get_date_range(period)
        end_date = timezone.now()
        
        # Agrupa vendas por mês
        vendas_por_mes = []
        
        # Se período for mês, mostra semanas
        if period == 'month':
            # Divide o mês em semanas
            current_date = start_date
            while current_date <= end_date:
                week_end = current_date + timedelta(days=6)
                if week_end > end_date:
                    week_end = end_date
                
                vendas_semana = Sale.objects.filter(
                    sale_date__date__gte=current_date.date(),
                    sale_date__date__lte=week_end.date(),
                    status='Done'
                )
                
                total = vendas_semana.aggregate(total=Sum('value'))['total'] or 0
                
                # Calcula crescimento em relação à semana anterior
                semana_anterior_inicio = current_date - timedelta(days=7)
                semana_anterior_fim = week_end - timedelta(days=7)
                vendas_anterior = Sale.objects.filter(
                    sale_date__date__gte=semana_anterior_inicio.date(),
                    sale_date__date__lte=semana_anterior_fim.date(),
                    status='Done'
                ).aggregate(total=Sum('value'))['total'] or 0
                
                crescimento = ((total - vendas_anterior) / vendas_anterior * 100) if vendas_anterior > 0 else 0
                
                vendas_por_mes.append({
                    'periodo': f"{current_date.strftime('%d/%m')} - {week_end.strftime('%d/%m')}",
                    'vendas': vendas_semana.count(),
                    'receita': float(total),
                    'comissoes': float(total * Decimal('0.03')),  # 3% de comissão
                    'crescimento': round(crescimento, 1)
                })
                
                current_date = week_end + timedelta(days=1)
        else:
            # Agrupa por mês
            current_date = start_date
            while current_date <= end_date:
                month_end = current_date.replace(
                    day=calendar.monthrange(current_date.year, current_date.month)[1]
                )
                
                vendas_mes = Sale.objects.filter(
                    sale_date__date__gte=current_date.date(),
                    sale_date__date__lte=month_end.date(),
                    status='Done'
                )
                
                total = vendas_mes.aggregate(total=Sum('value'))['total'] or 0
                
                # Calcula crescimento em relação ao mês anterior
                mes_anterior = current_date - timedelta(days=1)
                mes_anterior = mes_anterior.replace(day=1)
                mes_anterior_fim = mes_anterior.replace(
                    day=calendar.monthrange(mes_anterior.year, mes_anterior.month)[1]
                )
                
                vendas_anterior = Sale.objects.filter(
                    sale_date__date__gte=mes_anterior.date(),
                    sale_date__date__lte=mes_anterior_fim.date(),
                    status='Done'
                ).aggregate(total=Sum('value'))['total'] or 0
                
                crescimento = ((total - vendas_anterior) / vendas_anterior * 100) if vendas_anterior > 0 else 0
                
                vendas_por_mes.append({
                    'periodo': current_date.strftime('%B %Y').capitalize(),
                    'vendas': vendas_mes.count(),
                    'receita': float(total),
                    'comissoes': float(total * Decimal('0.03')),  # 3% de comissão
                    'crescimento': round(crescimento, 1)
                })
                
                # Próximo mês
                next_month = current_date.month + 1
                next_year = current_date.year
                if next_month > 12:
                    next_month = 1
                    next_year += 1
                current_date = current_date.replace(year=next_year, month=next_month, day=1)
        
        return vendas_por_mes
    
    @staticmethod
    def get_dados_graficos(period='month'):
        """Dados para gráficos"""
        start_date = ReportService.get_date_range(period)
        end_date = timezone.now()
        
        # Dados para gráfico de linhas (vendas por período)
        labels = []
        dados_vendas = []
        
        if period == 'month':
            # Últimos 30 dias
            for i in range(30):
                date = end_date - timedelta(days=29 - i)
                count = Sale.objects.filter(
                    sale_date__date=date.date(),
                    status='Done'
                ).count()
                labels.append(date.strftime('%d/%m'))
                dados_vendas.append(count)
        else:
            # Últimos 6 meses
            for i in range(5, -1, -1):
                date = end_date - timedelta(days=30 * i)
                count = Sale.objects.filter(
                    sale_date__year=date.year,
                    sale_date__month=date.month,
                    status='Done'
                ).count()
                labels.append(date.strftime('%b/%Y'))
                dados_vendas.append(count)
        
        # Dados para gráfico de pizza (vendas por marca)
        vendas_marca = Sale.objects.filter(
            sale_date__gte=start_date,
            status='Done'
        ).values(
            'vehicle__mark'
        ).annotate(
            total=Count('id')
        ).order_by('-total')[:5]
        
        pizza_labels = [v['vehicle__mark'] or 'Outros' for v in vendas_marca]
        pizza_dados = [v['total'] for v in vendas_marca]
        
        return {
            'line_chart': {
                'labels': labels,
                'datasets': [{
                    'label': 'Vendas',
                    'data': dados_vendas,
                    'borderColor': '#06b6d4',
                    'backgroundColor': 'rgba(6, 182, 212, 0.1)',
                }]
            },
            'pie_chart': {
                'labels': pizza_labels,
                'datasets': [{
                    'data': pizza_dados,
                    'backgroundColor': ['#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b'],
                }]
            }
        }