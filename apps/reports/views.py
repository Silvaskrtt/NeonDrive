from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services import ReportService
from .models import SavedReport
from .serializers import SavedReportSerializer
import csv
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import traceback
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

class ReportsView(LoginRequiredMixin, TemplateView):
    """View principal da página de relatórios"""
    template_name = 'reports/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Relatórios'
        return context

class ReportsAPIView(APIView):
    """API para dados dos relatórios"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            period = request.GET.get('period', 'month')
            
            return Response({
                'vendas_por_marca': ReportService.get_vendas_por_marca(period),
                'performance_vendedores': ReportService.get_performance_vendedores(period),
                'metricas_gerais': ReportService.get_metricas_gerais(period),
                'relatorio_detalhado': ReportService.get_relatorio_detalhado(period),
                'dados_graficos': ReportService.get_dados_graficos(period),
            })
            
        except Exception as e:
            print(f"❌ ERRO: {str(e)}")
            traceback.print_exc()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ExportReportView(LoginRequiredMixin, View):
    """Exportar relatório usando View do Django em vez de APIView"""
    
    def get(self, request):
        print("\n" + "="*50)
        print("🎯 ExportReportView.get() EXECUTADO!")
        print(f"Path: {request.path}")
        print(f"User: {request.user}")
        print(f"Autenticado: {request.user.is_authenticated}")
        print(f"GET params: {dict(request.GET)}")
        print("="*50 + "\n")
        
        format = request.GET.get('format', 'excel')
        period = request.GET.get('period', 'month')
        
        try:
            if format == 'excel':
                return self.export_excel(period)
            elif format == 'csv':
                return self.export_csv(period)
            elif format == 'pdf':
                return self.export_pdf(period)
            else:
                return HttpResponse('Formato não suportado', status=400)
        except Exception as e:
            print(f"❌ Erro: {e}")
            import traceback
            traceback.print_exc()
            return HttpResponse(f'Erro: {e}', status=500)
    
    def export_excel(self, period):
        # Seu código existente de export_excel
        from .services import ReportService
        from django.utils import timezone
        import openpyxl
        from openpyxl.styles import Font, Alignment, PatternFill
        from io import BytesIO
        
        dados = ReportService.get_relatorio_detalhado(period)
        metricas = ReportService.get_metricas_gerais(period)
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Relatório de Vendas"
        
        # Título
        ws.merge_cells('A1:E1')
        ws['A1'] = f"Relatório de Vendas - {timezone.now().strftime('%d/%m/%Y')}"
        ws['A1'].font = Font(size=14, bold=True)
        ws['A1'].alignment = Alignment(horizontal='center')
        
        # Métricas
        ws['A3'] = "Métricas Gerais"
        ws['A3'].font = Font(bold=True)
        
        metrics_data = [
            ['Ticket Médio', f"R$ {metricas['ticket_medio']:,.2f}"],
            ['Taxa de Conversão', f"{metricas['taxa_conversao']}%"],
            ['Leads no Mês', metricas['leads_mes']],
            ['Total de Vendas', metricas['total_vendas']],
        ]
        
        for i, (label, value) in enumerate(metrics_data):
            ws[f'A{4+i}'] = label
            ws[f'B{4+i}'] = value
        
        # Cabeçalho
        headers = ['Período', 'Vendas', 'Receita', 'Comissões', 'Crescimento']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=7, column=col)
            cell.value = header
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="06b6d4", end_color="06b6d4", fill_type="solid")
            cell.alignment = Alignment(horizontal='center')
        
        # Dados
        for row, item in enumerate(dados, 8):
            ws.cell(row=row, column=1).value = item['periodo']
            ws.cell(row=row, column=2).value = item['vendas']
            ws.cell(row=row, column=3).value = item['receita']
            ws.cell(row=row, column=4).value = item['comissoes']
            ws.cell(row=row, column=5).value = f"{item['crescimento']}%"
            ws.cell(row=row, column=3).number_format = 'R$ #,##0.00'
            ws.cell(row=row, column=4).number_format = 'R$ #,##0.00'
        
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="relatorio_vendas_{timezone.now().strftime("%Y%m%d")}.xlsx"'
        return response
    
    def export_csv(self, period):
        # Seu código existente de export_csv
        from .services import ReportService
        import csv
        from django.utils import timezone
        
        dados = ReportService.get_relatorio_detalhado(period)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="relatorio_vendas_{timezone.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Período', 'Vendas', 'Receita', 'Comissões', 'Crescimento'])
        
        for item in dados:
            writer.writerow([
                item['periodo'],
                item['vendas'],
                f"R$ {item['receita']:,.2f}",
                f"R$ {item['comissoes']:,.2f}",
                f"{item['crescimento']}%"
            ])
        
        return response
    
    def export_pdf(self, period):
        # Seu código existente de export_pdf
        from .services import ReportService
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        from io import BytesIO
        from django.utils import timezone
        
        dados = ReportService.get_relatorio_detalhado(period)
        metricas = ReportService.get_metricas_gerais(period)
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        title = Paragraph(f"Relatório de Vendas - {timezone.now().strftime('%d/%m/%Y')}", styles['Title'])
        elements.append(title)
        elements.append(Paragraph("<br/>", styles['Normal']))
        
        elements.append(Paragraph("Métricas Gerais", styles['Heading2']))
        metrics_data = [
            ['Ticket Médio:', f"R$ {metricas['ticket_medio']:,.2f}"],
            ['Taxa de Conversão:', f"{metricas['taxa_conversao']}%"],
            ['Leads no Mês:', str(metricas['leads_mes'])],
            ['Total de Vendas:', str(metricas['total_vendas'])],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[150, 150])
        metrics_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        elements.append(metrics_table)
        elements.append(Paragraph("<br/><br/>", styles['Normal']))
        
        elements.append(Paragraph("Vendas por Período", styles['Heading2']))
        
        table_data = [['Período', 'Vendas', 'Receita', 'Comissões', 'Crescimento']]
        for item in dados:
            table_data.append([
                item['periodo'],
                str(item['vendas']),
                f"R$ {item['receita']:,.2f}",
                f"R$ {item['comissoes']:,.2f}",
                f"{item['crescimento']}%"
            ])
        
        table = Table(table_data, colWidths=[120, 60, 100, 100, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.cyan),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        
        doc.build(elements)
        
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="relatorio_vendas_{timezone.now().strftime("%Y%m%d")}.pdf"'
        return response

class SavedReportsView(APIView):
    """Views para relatórios salvos"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        reports = SavedReport.objects.filter(created_by=request.user)
        serializer = SavedReportSerializer(reports, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data.copy()
        data['created_by'] = request.user.id
        
        serializer = SavedReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@csrf_exempt
def exportar_direto(request):
    """View direta sem APIView para teste"""
    print("\n" + "="*50)
    print("🚨 VIEW DIRETA FOI CHAMADA!")
    print(f"Path: {request.path}")
    print(f"Method: {request.method}")
    print(f"User: {request.user}")
    print(f"Autenticado: {request.user.is_authenticated}")
    print(f"GET: {dict(request.GET)}")
    print("="*50 + "\n")
    
    format = request.GET.get('format', 'excel')
    period = request.GET.get('period', 'month')
    
    # Simula um arquivo para teste
    response = HttpResponse(
        f"Teste de exportação - Formato: {format}, Período: {period}\nData: {timezone.now()}",
        content_type='text/plain'
    )
    response['Content-Disposition'] = f'attachment; filename="teste_{format}.txt"'
    return response