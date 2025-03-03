from django.urls import path
from django.views.decorators.cache import cache_page

from .views import MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, MessageDetailView, \
    MailingListView, MailingCreateView, MailingUpdateView, MailingDetailView, MailingDeleteView


urlpatterns = [
    path('messages/', cache_page(60)(MessageListView.as_view()), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/edit/', MessageUpdateView.as_view(), name='message_edit'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('mailings/', cache_page(60)(MailingListView.as_view()), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
]
