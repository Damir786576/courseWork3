from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.core.cache import cache
from .models import Message, Mailing
from .forms import MessageForm, MailingForm


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailings/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        cache_key = f'message_list_{self.request.user.id}'
        messages = cache.get(cache_key)
        if not messages:
            if self.request.user.is_staff:
                messages = Message.objects.all()
            else:
                messages = Message.objects.filter(owner=self.request.user)
            cache.set(cache_key, messages, timeout=300)
        return messages


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message_create.html'
    success_url = reverse_lazy('message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        cache.delete(f'message_list_{self.request.user.id}')
        return response


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('message_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or obj.owner == self.request.user or self.request.user.groups.filter(
            name='Менеджеры').exists()

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete(f'message_list_{self.request.user.id}')
        return response


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message
    template_name = 'mailings/message_detail.html'
    context_object_name = 'message'

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or obj.owner == self.request.user or self.request.user.groups.filter(
            name='Менеджеры').exists()


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or obj.owner == self.request.user or self.request.user.groups.filter(
            name='Менеджеры').exists()

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        cache.delete(f'message_list_{self.request.user.id}')
        return response


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        cache_key = f'mailing_list_{self.request.user.id}'
        mailings = cache.get(cache_key)
        if not mailings:
            if self.request.user.is_staff or self.request.user.groups.filter(name='Менеджеры').exists():
                mailings = Mailing.objects.all()
            else:
                mailings = Mailing.objects.filter(owner=self.request.user)
            cache.set(cache_key, mailings, timeout=300)
        return mailings


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        cache.delete(f'mailing_list_{self.request.user.id}')
        return response


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or obj.owner == self.request.user or self.request.user.has_perm(
            'mailings.change_all_mailings') or self.request.user.groups.filter(name='Менеджеры').exists()

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete(f'mailing_list_{self.request.user.id}')
        return response


class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or obj.owner == self.request.user or self.request.user.groups.filter(
            name='Менеджеры').exists()


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or obj.owner == self.request.user or self.request.user.groups.filter(
            name='Менеджеры').exists()

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        cache.delete(f'mailing_list_{self.request.user.id}')
        return response
