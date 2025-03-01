from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('clients/', include('clients.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('mailings/', include('mailings.urls')),
    path("users/", include("users.urls", namespace="users")),
]
