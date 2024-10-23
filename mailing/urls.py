from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (MailingView, RecipientListView, RecipientDetailView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView)


app_name = MailingConfig.name

urlpatterns = [
    path("main/", MailingView.as_view(), name="main"),
    path("main/recipients", RecipientListView.as_view(), name="recipient_list"),
    path("main/recipients/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("main/recipients/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("main/recipients/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("main/recipients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
]
