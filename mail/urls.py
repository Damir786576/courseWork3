from django.urls import path

from mail.views import index

urlpatterns = [
    path('', index)
]
