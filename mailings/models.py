from django.core.mail import send_mail
from django.utils import timezone

from django.db import models
from clients.models import Clients
from users.models import User


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)

    def __str__(self):
        return self.subject

    class Meta:
        permissions = [
            ("view_all_messages", "Может просматривать все сообщения"),
            ("change_all_messages", "Может редактировать все сообщения"),
        ]


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    subject = models.CharField(max_length=255)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Clients)
    first_sent_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')

    def __str__(self):
        return self.subject

    def send(self):
        self.status = 'started'
        self.first_sent_at = timezone.now()
        self.save()

        for client in self.clients.all():
            try:
                send_mail(
                    self.message.subject,
                    self.message.body,
                    'rilz.snep@yandex.ru',
                    [client.email],
                    fail_silently=False,
                )
                print(f'Сообщение для {client.email} отправлено успешно.')

                # Сохраняем успешную попытку
                CampaignAttempt.objects.create(
                    mailing=self,
                    status='status_ok',
                    server_response="Email отправлен успешно",
                )
            except Exception as e:
                self.status = 'failed'
                self.save()
                print(f'Ошибка при отправке на {client.email}: {e}')

                # Сохраняем неуспешную попытку
                CampaignAttempt.objects.create(
                    mailing=self,
                    status='status_nok',
                    server_response=str(e),
                )

        self.status = 'completed'
        self.end_at = timezone.now()
        self.save()
        print(f'Рассылка "{self.subject}" завершена.')

    class Meta:
        permissions = [
            ("change_all_mailings", "Can change all mailings"),
        ]


class CampaignAttempt(models.Model):
    STATUS_CHOICES = [
        ('status_ok', 'Успешно'),
        ('status_nok', 'Не успешно'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name="attempts")
    date_attempt = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField()

    def __str__(self):
        return f"Попытка {self.status} - {self.date_attempt}"
