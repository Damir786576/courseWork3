from django.contrib import admin
from users.models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_staff")
    filter_horizontal = ('groups',)