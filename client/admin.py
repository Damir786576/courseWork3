from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name")
    search_fields = ("email", "full_name")
