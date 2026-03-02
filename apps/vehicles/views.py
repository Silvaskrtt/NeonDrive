# apps/vehicles/views.py

from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Vehicle
from django.http import JsonResponse
from .forms import VehicleForm


# ============================================
# VIEW DE BUSCA EM TEMPO REAL
# ============================================

class VehicleSearchJSON(LoginRequiredMixin, View):
    """Retorna veículos filtrados em JSON para busca em tempo real"""
    
    def get(self, request):
        search = request.GET.get('search', '')
        
        # Filtra os veículos
        vehicles = Vehicle.objects.all()
        if search:
            vehicles = vehicles.filter(
                models.Q(mark__icontains=search) |
                models.Q(model__icontains=search) |
                models.Q(car_plate__icontains=search) |
                models.Q(color__icontains=search)
            )
        
        # Ordena por data de criação (mais recentes primeiro)
        vehicles = vehicles.order_by('-created_at')
        
        # Prepara os dados para JSON
        data = []
        for vehicle in vehicles:
            data.append({
                'id': vehicle.id,
                'mark': vehicle.mark,
                'model': vehicle.model,
                'year': vehicle.year,
                'car_plate': vehicle.car_plate,
                'color': vehicle.color,
                'value': str(vehicle.value),
                'status': vehicle.status,
                'status_display': vehicle.get_status_display(),
                'image_url': vehicle.image.url if vehicle.image else None,
                'created_at': vehicle.created_at.strftime('%d/%m/%Y'),
            })
        
        return JsonResponse({'vehicles': data})


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
                return redirect('vehicles:list')
        except:
            messages.error(request, 'Perfil não encontrado.')
            return redirect('vehicles:list')
        return super().dispatch(request, *args, **kwargs)


# ============================================
# VIEWS DE VEÍCULOS COM PERMISSÕES
# ============================================

class VehicleList(LoginRequiredMixin, ListView):
    """
    Lista de veículos - todos podem ver
    - LoginRequired: apenas usuários logados
    """
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 20
    
    def get_queryset(self):
        """Permite buscar veículos"""
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(mark__icontains=search) |
                models.Q(model__icontains=search) |
                models.Q(car_plate__icontains=search) |
                models.Q(color__icontains=search)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class VehicleDetail(LoginRequiredMixin, DetailView):
    """
    Detalhe do veículo - todos podem ver
    - LoginRequired: apenas usuários logados
    """
    model = Vehicle
    template_name = 'vehicles/vehicle_detail.html'
    context_object_name = 'vehicle'


class VehicleDetailJSON(LoginRequiredMixin, View):
    """Retorna dados do veículo em JSON para o modal"""
    
    def get(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
            data = {
                'id': vehicle.id,
                'mark': vehicle.mark,
                'model': vehicle.model,
                'year': vehicle.year,
                'car_plate': vehicle.car_plate,
                'color': vehicle.color,
                'value': str(vehicle.value),
                'status': vehicle.status,
                'status_display': vehicle.get_status_display(),
                'image_url': vehicle.image.url if vehicle.image else None,
                'created_at': vehicle.created_at.strftime('%d/%m/%Y'),
            }
            return JsonResponse(data)
        except Vehicle.DoesNotExist:
            return JsonResponse({'error': 'Veículo não encontrado'}, status=404)


class VehicleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Criar veículo - apenas quem tem permissão
    - Permissions: vehicles.add_vehicle
    """
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicles:list')
    permission_required = 'vehicles.add_vehicle'
    
    def form_valid(self, form):
        """Associa o usuário logado e mostra mensagem de sucesso"""
        form.instance.user = self.request.user
        messages.success(self.request, 'Veículo criado com sucesso!')
        return super().form_valid(form)


class VehicleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Editar veículo - apenas quem tem permissão
    - Permissions: vehicles.change_vehicle
    """
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicles:list')
    permission_required = 'vehicles.change_vehicle'
    
    def form_valid(self, form):
        """Mensagem de sucesso ao editar"""
        messages.success(self.request, 'Veículo atualizado com sucesso!')
        return super().form_valid(form)


class VehicleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Deletar veículo - apenas quem tem permissão
    - Permissions: vehicles.delete_vehicle
    """
    model = Vehicle
    template_name = 'vehicles/vehicle_confirm_delete.html'
    success_url = reverse_lazy('vehicles:list')
    permission_required = 'vehicles.delete_vehicle'
    
    def delete(self, request, *args, **kwargs):
        """Mensagem de sucesso ao deletar"""
        messages.success(request, 'Veículo removido com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============================================
# VERSÕES COM ROLE (caso queira usar role em vez de permissões)
# ============================================

class VehicleCreateByRole(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Criar veículo baseado em role (ADMIN apenas)"""
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicles:list')
    allowed_roles = ['ADMIN']  # Apenas ADMIN pode criar


class VehicleUpdateByRole(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """Editar veículo baseado em role (ADMIN e USER)"""
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicles:list')
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
    template_name = 'vehicles/vehicle_manage.html'
    permission_required = 'vehicles.change_vehicle'
    allowed_roles = ['ADMIN']  # Só ADMIN pode, mesmo com permissão