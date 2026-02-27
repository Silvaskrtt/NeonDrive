from django.shortcuts import render
from apps.clients.models import Client
from django.contrib.auth.decorators import login_required

@login_required
def client_report(request):

    clients = Client.objects.all()

    return render(request, 'reports/client_report.html', {
        'clients': clients
    })