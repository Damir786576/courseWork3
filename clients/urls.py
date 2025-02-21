from django.urls import path
from .views import ClientsListView, ClientsCreateView, ClientsUpdateView, ClientsDeleteView, ClientsDetailView

urlpatterns = [
    path('clients/', ClientsListView.as_view(), name='clients_list'),
    path('create/', ClientsCreateView.as_view(), name='clients_create'),
    path('<int:pk>/', ClientsDetailView.as_view(), name='clients_detail'),
    path('<int:pk>/edit/', ClientsUpdateView.as_view(), name='clients_edit'),
    path('<int:pk>/delete/', ClientsDeleteView.as_view(), name='clients_delete'),
]
