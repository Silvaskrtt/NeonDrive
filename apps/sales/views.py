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
            if request.user.profile.role in self.allowed_roles:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, 'Acesso negado. Você não tem permissão.')
                return redirect('sales:list')
        except:
            messages.error(request, 'Perfil não encontrado.')
            return redirect('sales:list')
        return super().dispatch(request, *args, **kwargs)


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
    paginate_by = 20
    
    def get_queryset(self):
        """Permite buscar vendas"""
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(client__name__icontains=search) |
                models.Q(vehicle__model__icontains=search) |
                models.Q(vehicle__plate__icontains=search)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class SaleDetail(LoginRequiredMixin, DetailView):
    """
    Detalhe do venda - todos podem ver
    - LoginRequired: apenas usuários logados
    """
    model = Sale
    template_name = 'sales/sale_detail.html'
    context_object_name = 'sale'
    

class SaleDetailJSON(LoginRequiredMixin, View):
    """Retorna dados do venda em JSON para o modal"""
    
    def get(self, request, pk):
        try:
            sale = Sale.objects.get(pk=pk)
            data = {
                'id': sale.id,
                'value': str(sale.value),
                'payment_method': dict(Sale.PAYMENT_CHOICES).get(sale.payment_method, sale.payment_method),
                'status': dict(Sale.STATUS_CHOICES).get(sale.status, sale.status),
                'sale_date': sale.sale_date.strftime('%d/%m/%Y %H:%M'),
                'user': sale.user.username if sale.user else 'N/A',
                'client': sale.client.name if sale.client else 'N/A',
                'vehicle': f"{sale.vehicle.model} - {sale.vehicle.plate}" if sale.vehicle else 'N/A',
            }
            return JsonResponse(data)
        except Sale.DoesNotExist:
            return JsonResponse({'error': 'Venda não encontrado'}, status=404)


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
    
    def form_valid(self, form):
        """Mensagem de sucesso ao criar"""
        form.instance.user = self.request.user
        messages.success(self.request, 'Venda criado com sucesso!')
        return super().form_valid(form)


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
    
    def form_valid(self, form):
        """Mensagem de sucesso ao editar"""
        messages.success(self.request, 'Venda atualizado com sucesso!')
        return super().form_valid(form)

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
        messages.success(request, 'Venda removido com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============================================
# VERSÕES COM ROLE (caso queira usar role em vez de permissões)
# ============================================

class SaleCreateByRole(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Criar venda baseado em role (ADMIN apenas)"""
    model = Sale
    fields = '__all__'
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:list')
    allowed_roles = ['ADMIN']  # Apenas ADMIN pode criar


class SaleUpdateByRole(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """Editar venda baseado em role (ADMIN e USER)"""
    model = Sale
    fields = '__all__'
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:list')
    allowed_roles = ['ADMIN', 'USER']  # ADMIN e USER podem editar


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
    permission_required = 'sales.change_sale'
    allowed_roles = ['ADMIN']  # Só ADMIN pode, mesmo com permissão# apps/sales/views.py

from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Sale

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
            if request.user.profile.role in self.allowed_roles:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, 'Acesso negado. Você não tem permissão.')
                return redirect('sales:list')
        except:
            messages.error(request, 'Perfil não encontrado.')
            return redirect('sales:list')
        return super().dispatch(request, *args, **kwargs)


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
    paginate_by = 20
    
    def get_queryset(self):
        """Permite buscar vendas"""
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class SaleDetail(LoginRequiredMixin, DetailView):
    """
    Detalhe do venda - todos podem ver
    - LoginRequired: apenas usuários logados
    """
    model = Sale
    template_name = 'sales/sale_detail.html'
    context_object_name = 'sale'


class SaleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Criar venda - apenas quem tem permissão
    - Permissions: sales.add_sale
    """
    model = Sale
    fields = ['name', 'email', 'phone', 'address', 'document']  # Especifique os campos
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:list')
    permission_required = 'sales.add_sale'
    
    def form_valid(self, form):
        """Mensagem de sucesso ao criar"""
        messages.success(self.request, 'Venda criada com sucesso!')
        return super().form_valid(form)


class SaleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Editar venda - apenas quem tem permissão
    - Permissions: sales.change_sale
    """
    model = Sale
    fields = ['name', 'email', 'phone', 'address', 'document']
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:list')
    permission_required = 'sales.change_sale'
    
    def form_valid(self, form):
        """Mensagem de sucesso ao editar"""
        messages.success(self.request, 'Venda atualizada com sucesso!')
        return super().form_valid(form)


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
    """Criar venda baseado em role (ADMIN apenas)"""
    model = Sale
    fields = '__all__'
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:list')
    allowed_roles = ['ADMIN']  # Apenas ADMIN pode criar


class SaleUpdateByRole(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """Editar vendas baseado em role (ADMIN e USER)"""
    model = Sale
    fields = '__all__'
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:list')
    allowed_roles = ['ADMIN', 'USER']  # ADMIN e USER podem editar


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
    permission_required = 'sales.change_sale'
    allowed_roles = ['ADMIN']  # Só ADMIN pode, mesmo com permissão