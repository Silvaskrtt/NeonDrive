# apps/clients/views.py

from django.shortcuts import render, redirect
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Client

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
                return redirect('clients:list')
        except:
            messages.error(request, 'Perfil não encontrado.')
            return redirect('clients:list')
        return super().dispatch(request, *args, **kwargs)


# ============================================
# VIEWS DE CLIENTES COM PERMISSÕES
# ============================================

class ClientList(LoginRequiredMixin, ListView):
    """
    Lista de clientes - todos podem ver
    - LoginRequired: apenas usuários logados
    """
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'
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


class ClientDetail(LoginRequiredMixin, DetailView):
    """
    Detalhe do cliente - todos podem ver
    - LoginRequired: apenas usuários logados
    """
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'


class ClientCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Criar cliente - apenas quem tem permissão
    - Permissions: clients.add_client
    """
    model = Client
    fields = ['name', 'email', 'phone', 'address', 'document']  # Especifique os campos
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')
    permission_required = 'clients.add_client'
    
    def form_valid(self, form):
        """Mensagem de sucesso ao criar"""
        messages.success(self.request, 'Cliente criado com sucesso!')
        return super().form_valid(form)


class ClientUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Editar cliente - apenas quem tem permissão
    - Permissions: clients.change_client
    """
    model = Client
    fields = ['name', 'email', 'phone', 'address', 'document']
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')
    permission_required = 'clients.change_client'
    
    def form_valid(self, form):
        """Mensagem de sucesso ao editar"""
        messages.success(self.request, 'Cliente atualizado com sucesso!')
        return super().form_valid(form)


class ClientDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Deletar cliente - apenas quem tem permissão
    - Permissions: clients.delete_client
    """
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('clients:list')
    permission_required = 'clients.delete_client'
    
    def delete(self, request, *args, **kwargs):
        """Mensagem de sucesso ao deletar"""
        messages.success(request, 'Cliente removido com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============================================
# VERSÕES COM ROLE (caso queira usar role em vez de permissões)
# ============================================

class ClientCreateByRole(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Criar cliente baseado em role (ADMIN apenas)"""
    model = Client
    fields = '__all__'
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')
    allowed_roles = ['ADMIN']  # Apenas ADMIN pode criar


class ClientUpdateByRole(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """Editar cliente baseado em role (ADMIN e USER)"""
    model = Client
    fields = '__all__'
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')
    allowed_roles = ['ADMIN', 'USER']  # ADMIN e USER podem editar


# ============================================
# VIEW COMBINANDO ROLE E PERMISSÕES
# ============================================

class ClientManage(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, DetailView):
    """
    View combinando role e permissões
    - Requer permissão E role específica
    """
    model = Client
    template_name = 'clients/client_manage.html'
    permission_required = 'clients.change_client'
    allowed_roles = ['ADMIN']  # Só ADMIN pode, mesmo com permissão# apps/clients/views.py

from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Client

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
                return redirect('clients:list')
        except:
            messages.error(request, 'Perfil não encontrado.')
            return redirect('clients:list')
        return super().dispatch(request, *args, **kwargs)


# ============================================
# VIEWS DE CLIENTES COM PERMISSÕES
# ============================================

class ClientList(LoginRequiredMixin, ListView):
    """
    Lista de clientes - todos podem ver
    - LoginRequired: apenas usuários logados
    """
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'
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


class ClientDetail(LoginRequiredMixin, DetailView):
    """
    Detalhe do cliente - todos podem ver
    - LoginRequired: apenas usuários logados
    """
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'


class ClientCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Criar cliente - apenas quem tem permissão
    - Permissions: clients.add_client
    """
    model = Client
    fields = ['name', 'email', 'phone', 'address', 'document']  # Especifique os campos
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')
    permission_required = 'clients.add_client'
    
    def form_valid(self, form):
        """Mensagem de sucesso ao criar"""
        messages.success(self.request, 'Cliente criado com sucesso!')
        return super().form_valid(form)


class ClientUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Editar cliente - apenas quem tem permissão
    - Permissions: clients.change_client
    """
    model = Client
    fields = ['name', 'email', 'phone', 'address', 'document']
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')
    permission_required = 'clients.change_client'
    
    def form_valid(self, form):
        """Mensagem de sucesso ao editar"""
        messages.success(self.request, 'Cliente atualizado com sucesso!')
        return super().form_valid(form)


class ClientDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Deletar cliente - apenas quem tem permissão
    - Permissions: clients.delete_client
    """
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('clients:list')
    permission_required = 'clients.delete_client'
    
    def delete(self, request, *args, **kwargs):
        """Mensagem de sucesso ao deletar"""
        messages.success(request, 'Cliente removido com sucesso!')
        return super().delete(request, *args, **kwargs)


# ============================================
# VERSÕES COM ROLE (caso queira usar role em vez de permissões)
# ============================================

class ClientCreateByRole(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Criar cliente baseado em role (ADMIN apenas)"""
    model = Client
    fields = '__all__'
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')
    allowed_roles = ['ADMIN']  # Apenas ADMIN pode criar


class ClientUpdateByRole(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """Editar cliente baseado em role (ADMIN e USER)"""
    model = Client
    fields = '__all__'
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')
    allowed_roles = ['ADMIN', 'USER']  # ADMIN e USER podem editar


# ============================================
# VIEW COMBINANDO ROLE E PERMISSÕES
# ============================================

class ClientManage(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, DetailView):
    """
    View combinando role e permissões
    - Requer permissão E role específica
    """
    model = Client
    template_name = 'clients/client_manage.html'
    permission_required = 'clients.change_client'
    allowed_roles = ['ADMIN']  # Só ADMIN pode, mesmo com permissão