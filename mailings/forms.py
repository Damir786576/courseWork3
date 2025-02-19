from django import forms
from clients.models import Clients
from .models import Message, Mailing


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        labels = {
            'subject': 'Тема письма',
            'body': 'Тело письма'
        }


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['subject', 'message', 'clients', 'first_sent_at', 'end_at', 'status']
        labels = {
            'subject': 'Тема рассылки',
            'message': 'Сообщение',
            'clients': 'Получатели',
            'first_sent_at': 'Дата и время начала',
            'end_at': 'Дата и время окончания',
            'status': 'Статус рассылки',
        }
        widgets = {
            'first_sent_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    clients = forms.ModelMultipleChoiceField(
        queryset=Clients.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите получателей"
    )
