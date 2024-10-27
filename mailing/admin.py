from django.contrib import admin
from .models import Recipient, Message, Mailing, Mailing_Attempts


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name", "comment")
    search_fields = ("email", "full_name")
    list_filter = ("email", "full_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "text")
    search_fields = ("subject",)
    list_filter = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_at", "end_at", "status", "message")
    search_fields = ("status", "message")
    list_filter = ("status", "message")


# Register your models here.
@admin.register(Mailing_Attempts)
class MailingAttemptsAdmin(admin.ModelAdmin):
    list_display = ("id", "attempt_date", "attempt_status", "mail_server_response", "mailing")
    search_fields = ("attempt_status", "mailing")
    list_filter = ("attempt_status", "mailing")
