# apps/vehicles/views.py

from django.shortcuts import render, redirect
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Vehicle

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
                return redirect('Vehicles:list')
        except:
            messages.error(request, 'Perfil não encontrado.')
            return redirect('Vehicles:list')
        return super().dispatch(request, *args, **kwargs)
    
# ============================================
# VIEWS DE CLIENTES COM PERMISSÕES
# ============================================

class VehicleList(LoginRequiredMixin, ListView):
    """
    Lista de veiculos - todos podem ver
    - LoginRequired: apenas usuários logados
    """
    model = Vehicle
    template_name = 'vehicles/vehicles_list.html'
    context_object_name = 'vehicles'
    paginate_by = 20
    
    def get_queryset(self):
        """Permite buscar clientes"""
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context
    
class VehicleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Criar veiculos - apenas quem tem permissão
    - Permissions: veiculos.add_vehicles
    """
    model = Vehicle
    fields = ['mark', 'model', 'year', 'car_plate', 'color', 'value', 'status'] 
    template_name = 'vehicles/vehicles_form.html'
    success_url = reverse_lazy('vehicles:list')
    permission_required = 'vehicles.add_vehicle'
    
    def form_valid(self, form):
        """Mensagem de sucesso ao criar"""
        messages.success(self.request, 'Veiculo criado com sucesso!')
        return super().form_valid(form)
    
class VehicleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Editar veiculo - apenas quem tem permissão
    - Permissions: vehicles.change_vehicle
    """
    model = Vehicle
    fields = ['mark', 'model', 'year', 'car_plate', 'color', 'value', 'status'] 
    template_name = 'vehicles/vehicles_form.html'
    success_url = reverse_lazy('vehicles:list')
    permission_required = 'vehicles.change_vehicle'
    
    def form_valid(self, form):
        """Mensagem de sucesso ao editar"""
        messages.success(self.request, 'Veiculo atualizado com sucesso!')
        return super().form_valid(form)
    
class VehicleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Deletar veiculo - apenas quem tem permissão
    - Permissions: Vehicles.delete_vehicle
    """
    model = Vehicle
    template_name = 'vehicle/vehicle_confirm_delete.html'
    success_url = reverse_lazy('vehicle:list')
    permission_required = 'vehicle.delete_vehicle'
    
    def delete(self, request, *args, **kwargs):
        """Mensagem de sucesso ao deletar"""
        messages.success(request, 'Veiculo removido com sucesso!')
        return super().delete(request, *args, **kwargs)
    

# ============================================
# VERSÕES COM ROLE (caso queira usar role em vez de permissões)
# ============================================

class VehicleCreateByRole(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Criar veiculos baseado em role (ADMIN apenas)"""
    model = Vehicle
    fields = '__all__'
    template_name = 'Vehicles/vehicle_form.html'
    success_url = reverse_lazy('Vehicles:list')
    allowed_roles = ['ADMIN']  # Apenas ADMIN pode criar


class VehicleUpdateByRole(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """Editar veiculos baseado em role (ADMIN e USER)"""
    model = Vehicle
    fields = '__all__'
    template_name = 'Vehicles/vehicle_form.html'
    success_url = reverse_lazy('Vehicles:list')
    allowed_roles = ['ADMIN', 'USER']  # ADMIN e USER podem editar


# ============================================
# VIEW COMBINANDO ROLE E PERMISSÕES
# ============================================

class VehicleManage(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, DetailView):
    """
    View combinando role e permissões
    - Requer permissão E role específica
    """
    model = Vehicle
    template_name = 'Vehicles/vehicle_manage.html'
    permission_required = 'Vehicles.change_vehicle'
    allowed_roles = ['ADMIN']  # Só ADMIN pode, mesmo com permissão# apps/Vehicles/views.py

# ============================================
# VERSÕES COM ROLE (caso queira usar role em vez de permissões)
# ============================================

class VehicleCreateByRole(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Criar veiculos baseado em role (ADMIN apenas)"""
    model = Vehicle
    fields = '__all__'
    template_name = 'Vehicles/vehicle_form.html'
    success_url = reverse_lazy('Vehicles:list')
    allowed_roles = ['ADMIN']  # Apenas ADMIN pode criar


class VehicleUpdateByRole(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """Editar veiculos baseado em role (ADMIN e USER)"""
    model = Vehicle
    fields = '__all__'
    template_name = 'Vehicles/vehicle_form.html'
    success_url = reverse_lazy('Vehicles:list')
    allowed_roles = ['ADMIN', 'USER']  # ADMIN e USER podem editar


# ============================================
# VIEW COMBINANDO ROLE E PERMISSÕES
# ============================================

class VehicleManage(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, DetailView):
    """
    View combinando role e permissões
    - Requer permissão E role específica
    """
    model = Vehicle
    template_name = 'Vehicles/vehicle_manage.html'
    permission_required = 'Vehicles.change_vehicle'
    allowed_roles = ['ADMIN']  # Só ADMIN pode, mesmo com permissão