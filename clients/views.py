from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from mailings.models import Mailing
from .models import Clients


def home(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='started').count()
    unique_recipients = Clients.objects.count()

    return render(request, 'clients/home.html', {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_recipients': unique_recipients
    })


class ClientsListView(ListView):
    model = Clients
    template_name = 'clients/clients_list.html'
    context_object_name = 'clients'


class ClientsDetailView(DetailView):
    model = Clients
    template_name = "clients/clients_detail.html"
    context_object_name = "client"


class ClientsCreateView(CreateView):
    model = Clients
    template_name = 'clients/clients_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('clients_list')


class ClientsUpdateView(UpdateView):
    model = Clients
    template_name = 'clients/clients_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('clients_list')


class ClientsDeleteView(DeleteView):
    model = Clients
    template_name = 'clients/clients_confirm_delete.html'
    success_url = reverse_lazy('clients_list')
