from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Client

class ClientList(LoginRequiredMixin, ListView):
    model = Client


class ClientCreate(LoginRequiredMixin, CreateView):
    model = Client
    fields = '__all__'
    success_url = '/clients/'


class ClientUpdate(LoginRequiredMixin, UpdateView):
    model = Client
    fields = '__all__'
    success_url = '/clients/'


class ClientDelete(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = '/clients/'