from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (
    MailingView,
)

app_name = MailingConfig.name

urlpatterns = [
    path("", MailingView.as_view(), name="mailing_list"),
]
