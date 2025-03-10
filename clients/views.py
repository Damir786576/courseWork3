from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.core.cache import cache
from mailings.models import Mailing, CampaignAttempt
from .models import Clients


def home(request):
    cache_key = f'home_stats_{request.user.id}'
    stats = cache.get(cache_key)
    if not stats:
        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status='started').count()
        unique_recipients = Clients.objects.filter(id__in=Mailing.objects.values('clients')).distinct().count()
        total_successful_attempts = CampaignAttempt.objects.filter(status='status_ok').count()
        total_unsuccessful_attempts = CampaignAttempt.objects.filter(status='status_nok').count()
        total_sent_messages = total_successful_attempts
        stats = {
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_recipients': unique_recipients,
            'total_successful_attempts': total_successful_attempts,
            'total_unsuccessful_attempts': total_unsuccessful_attempts,
            'total_sent_messages': total_sent_messages,
        }
        cache.set(cache_key, stats, timeout=300)
    return render(request, 'clients/home.html', stats)


def campaign_attempts(request):
    cache_key = f'campaign_attempts_{request.user.id}'
    attempts = cache.get(cache_key)
    if not attempts:
        if request.user.is_staff:
            attempts = CampaignAttempt.objects.all()
        else:
            attempts = CampaignAttempt.objects.filter(mailing__owner=request.user)
        cache.set(cache_key, attempts, timeout=300)
    return render(request, 'clients/campaign_attempts.html', {'attempts': attempts})


class ClientsListView(LoginRequiredMixin, ListView):
    model = Clients
    template_name = 'clients/clients_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        cache_key = f'clients_list_{self.request.user.id}'
        clients = cache.get(cache_key)
        if not clients:
            if self.request.user.is_staff:
                clients = Clients.objects.all()
            else:
                clients = Clients.objects.filter(owner=self.request.user)
            cache.set(cache_key, clients, timeout=300)
        return clients


class ClientsDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Clients
    template_name = "clients/clients_detail.html"
    context_object_name = "clients"

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or obj.owner == self.request.user


class ClientsCreateView(LoginRequiredMixin, CreateView):
    model = Clients
    template_name = 'clients/clients_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('clients_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        cache.delete(f'clients_list_{self.request.user.id}')
        return response


class ClientsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Clients
    template_name = 'clients/clients_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('clients_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or obj.owner == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete(f'clients_list_{self.request.user.id}')
        return response


class ClientsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Clients
    template_name = 'clients/clients_confirm_delete.html'
    success_url = reverse_lazy('clients_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or obj.owner == self.request.user

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        cache.delete(f'clients_list_{self.request.user.id}')
        return response


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect("users:login")
