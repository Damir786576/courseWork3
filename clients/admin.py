from django.contrib import admin
from .models import Clients


@admin.register(Clients)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')
    search_fields = ('email', 'full_name')
