from django.shortcuts import render
from clients.models import Client
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def home(request):

    context = {
        'total_clients': Client.objects.count(),
        'total_users': User.objects.count(),
        'recent_clients': Client.objects.order_by('-created_at')[:5]
    }

    return render(request, 'dashboard/home.html', context)