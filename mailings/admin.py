from django.contrib import admin
from .models import Message, Mailing, CampaignAttempt


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
    )
    search_fields = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'first_sent_at', 'end_at', 'status', 'owner')
    list_filter = ('status', 'first_sent_at')
    search_fields = ('subject', 'message')
    ordering = ('-first_sent_at',)
    filter_horizontal = ('clients',)

    fieldsets = (
        ("Основная информация", {
            'fields': ('subject', 'message', 'clients')
        }),
        ("Настройки рассылки", {
            'fields': ('first_sent_at', 'end_at', 'status'),
        }),
    )

    actions = ['send_mailing']

    def send_mailing(self, request, queryset):
        for mailing in queryset:
            if mailing.status == 'created':
                mailing.send()
                self.message_user(request, f'Рассылка "{mailing.subject}" отправлена!')
            else:
                self.message_user(request, f'Рассылка "{mailing.subject}" уже была отправлена или в процессе!')

    send_mailing.short_description = "Отправить рассылку вручную"


@admin.register(CampaignAttempt)
class CampaignAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'date_attempt', 'status', 'server_response')
    list_filter = ('status', 'date_attempt')
    search_fields = ('mailing__subject', 'server_response')
