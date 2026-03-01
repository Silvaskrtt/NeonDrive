# apps/sales/views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import models
from .models import Sale
from .forms import SaleForm

# ============================================
# MIXIN PERSONALIZADO PARA ROLE
# ============================================

class RoleRequiredMixin:
    """Mixin para verificar role do usuário"""
    allowed_roles = []
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        try:
            if hasattr(request.user, 'profile') and request.user.profile.role in self.allowed_roles:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, 'Acesso negado. Você não tem permissão para acessar esta página.')
                return redirect('sales:list')
        except Exception as e:
            messages.error(request, 'Erro ao verificar perfil do usuário.')
            return redirect('sales:list')


# ============================================
# VIEWS DE VENDAS COM PERMISSÕES
# ============================================

class SaleList(LoginRequiredMixin, ListView):
    """
    Lista de vendas - todos podem ver
    - LoginRequired: apenas usuários logados
    """
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'
    paginate_by = 10
    
    def get_queryset(self):
        """Permite buscar vendas"""
        queryset = super().get_queryset().select_related('client', 'vehicle', 'user')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(client__name__icontains=search) |
                models.Q(vehicle__model__icontains=search) |
                models.Q(vehicle__plate__icontains=search) |
                models.Q(user__username__icontains=search)
            )
        return queryset.order_by('-sale_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['can_add'] = self.request.user.has_perm('sales.add_sale')
        context['can_change'] = self.request.user.has_perm('sales.change_sale')
        context['can_delete'] = self.request.user.has_perm('sales.delete_sale')
        return context


class SaleDetail(LoginRequiredMixin, DetailView):
    """
    Detalhe da venda - todos podem ver
    - LoginRequired: apenas usuários logados
    """
    model = Sale
    template_name = 'sales/sale_detail.html'
    context_object_name = 'sale'
    
    def get_queryset(self):
        return super().get_queryset().select_related('client', 'vehicle', 'user')


class SaleDetailJSON(LoginRequiredMixin, View):
    """Retorna dados da venda em JSON para o modal"""
    
    def get(self, request, pk):
        try:
            sale = Sale.objects.select_related('client', 'vehicle', 'user').get(pk=pk)
            
            # Mapeamento de status para exibição
            status_display = {
                'Pending': 'Pendente',
                'Done': 'Concluída',
                'Canceled': 'Cancelada'
            }
            
            data = {
                'id': sale.id,
                'value': str(sale.value),
                'payment_method': dict(Sale.PAYMENT_CHOICES).get(sale.payment_method, sale.payment_method),
                'status': status_display.get(sale.status, sale.status),
                'status_code': sale.status,
                'sale_date': sale.sale_date.strftime('%d/%m/%Y %H:%M'),
                'user': sale.user.get_full_name() or sale.user.username if sale.user else 'N/A',
                'client': {
                    'id': sale.client.id,
                    'name': sale.client.name,
                    'email': getattr(sale.client, 'email', 'N/A'),
                    'phone': getattr(sale.client, 'phone', 'N/A'),
                    'document': getattr(sale.client, 'document', 'N/A'),
                } if sale.client else None,
                'vehicle': {
                    'id': sale.vehicle.id,
                    'model': sale.vehicle.model,
                    'plate': sale.vehicle.plate,
                    'year': getattr(sale.vehicle, 'year', 'N/A'),
                    'color': getattr(sale.vehicle, 'color', 'N/A'),
                    'brand': getattr(sale.vehicle, 'brand', 'N/A'),
                } if sale.vehicle else None,
            }
            return JsonResponse(data)
        except Sale.DoesNotExist:
            return JsonResponse({'error': 'Venda não encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class SaleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Criar venda - apenas quem tem permissão
    - Permissions: sales.add_sale
    """
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:list')
    permission_required = 'sales.add_sale'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        """Mensagem de sucesso ao criar"""
        form.instance.user = self.request.user
        messages.success(self.request, 'Venda criada com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Mensagem de erro ao criar"""
        messages.error(self.request, 'Erro ao criar venda. Verifique os dados informados.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nova Venda'
        context['button_text'] = 'Criar Venda'
        return context


class SaleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Editar venda - apenas quem tem permissão
    - Permissions: sales.change_sale
    """
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:list')
    permission_required = 'sales.change_sale'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        """Mensagem de sucesso ao editar"""
        messages.success(self.request, 'Venda atualizada com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Mensagem de erro ao editar"""
        messages.error(self.request, 'Erro ao atualizar venda. Verifique os dados informados.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Venda'
        context['button_text'] = 'Atualizar Venda'
        return context


class SaleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Deletar venda - apenas quem tem permissão
    - Permissions: sales.delete_sale
    """
    model = Sale
    template_name = 'sales/sale_confirm_delete.html'
    success_url = reverse_lazy('sales:list')
    permission_required = 'sales.delete_sale'
    
    def delete(self, request, *args, **kwargs):
        """Mensagem de sucesso ao deletar"""
        messages.success(request, 'Venda removida com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============================================
# VERSÕES COM ROLE (caso queira usar role em vez de permissões)
# ============================================

class SaleCreateByRole(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Criar venda baseado em role"""
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:list')
    allowed_roles = ['ADMIN']  # Apenas ADMIN pode criar
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Venda criada com sucesso!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nova Venda'
        context['button_text'] = 'Criar Venda'
        return context


class SaleUpdateByRole(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """Editar venda baseado em role"""
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:list')
    allowed_roles = ['ADMIN', 'USER']  # ADMIN e USER podem editar
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Venda atualizada com sucesso!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Venda'
        context['button_text'] = 'Atualizar Venda'
        return context


class SaleDeleteByRole(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    """Deletar venda baseado em role"""
    model = Sale
    template_name = 'sales/sale_confirm_delete.html'
    success_url = reverse_lazy('sales:list')
    allowed_roles = ['ADMIN']  # Apenas ADMIN pode deletar
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Venda removida com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============================================
# VIEW COMBINANDO ROLE E PERMISSÕES
# ============================================

class SaleManage(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, DetailView):
    """
    View combinando role e permissões
    - Requer permissão E role específica
    """
    model = Sale
    template_name = 'sales/sale_manage.html'
    context_object_name = 'sale'
    permission_required = 'sales.change_sale'
    allowed_roles = ['ADMIN']  # Só ADMIN pode, mesmo com permissão
    
    def get_queryset(self):
        return super().get_queryset().select_related('client', 'vehicle', 'user')