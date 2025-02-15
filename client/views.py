from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from client.forms import ClientsForm
from client.models import Clients
from mailing.models import Campaign


class HomeView(TemplateView):
    template_name = "clients/home.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(
                request, "clients/home.html"
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["count_campaign"] = Campaign.objects.count()
        context_data["active_campaign_count"] = Campaign.objects.filter(status="started").count()
        unique_clients_count = Campaign.objects.values("recipients").distinct().count()
        context_data["unique_clients_count"] = unique_clients_count

        user = self.request.user
        user_campaigns = Campaign.objects.filter(owner=user)
        context_data["total_successful_attempts"] = (
            user_campaigns.aggregate(Sum("successful_attempts"))[
                "successful_attempts__sum"
            ]
            or 0
        )
        context_data["total_unsuccessful_attempts"] = (
            user_campaigns.aggregate(Sum("unsuccessful_attempts"))[
                "unsuccessful_attempts__sum"
            ]
            or 0
        )
        context_data["total_sent_messages"] = (
            user_campaigns.aggregate(Sum("sent_messages"))["sent_messages__sum"] or 0
        )
        return context_data


class ClientsListView(LoginRequiredMixin, ListView):
    model = Clients
    template_name = "clients/clients_list.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm("clients.view_clients"):
            return HttpResponseForbidden(
                "У вас нет прав для просмотра списка клиентов."
            )
        return super().dispatch(request, *args, **kwargs)


class ClientsDetailView(DetailView):
    model = Clients


class ClientsDeleteView(DeleteView):
    model = Clients
    success_url = reverse_lazy("clients:clients_list")


class ClientsUpdateView(UpdateView):
    model = Clients
    form_class = ClientsForm
    success_url = reverse_lazy("clients:clients_list")


class ClientsCreateView(CreateView):
    model = Clients
    form_class = ClientsForm
    success_url = reverse_lazy("clients:clients_list")
