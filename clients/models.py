from django.db import models

from users.models import User


class Clients(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        permissions = [
            ("view_all_clients", "Может просматривать всех клиентов"),
            ("change_all_clients", "Может редактировать всех клиентов"),
        ]

    def __str__(self):
        return self.full_name
