from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (MailingView, RecipientListView, RecipientDetailView, RecipientCreateView,
                           RecipientUpdateView, RecipientDeleteView, MessageListView, MessageDetailView,
                           MessageCreateView, MessageUpdateView, MessageDeleteView,
                           MailingCreateView, MailingUpdateView, MailingDeleteView,
                           MailingDetailView, MailingListView)


app_name = MailingConfig.name

urlpatterns = [
    path("main/", MailingView.as_view(), name="main"),
    path("main/recipients", RecipientListView.as_view(), name="recipient_list"),
    path("main/recipients/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("main/recipients/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("main/recipients/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("main/recipients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),

    path("main/messages", MessageListView.as_view(), name="message_list"),
    path("main/messages/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("main/messages/create/", MessageCreateView.as_view(), name="message_create"),
    path("main/messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("main/messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),

    path("main/mailing", MailingListView.as_view(), name="mailing_list"),
    path("main/mailing/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("main/mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("main/mailing/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("main/mailing/<int:pk>/delete/", MailingDeleteView.as_view(),

]
