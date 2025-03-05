from django.contrib import admin
from django.urls import path, include
from clients.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path('clients/', include('clients.urls')),
    path('', home, name='home'),
    path('mailings/', include('mailings.urls')),
    path("users/", include("users.urls", namespace="users")),
]