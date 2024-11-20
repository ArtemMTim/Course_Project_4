from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        managers = Group.objects.create(name="managers")
        view_users = Permission.objects.get(codename="view_user")
        view_mailing = Permission.objects.get(codename="view_mailing")
        view_recipient = Permission.objects.get(codename="view_recipient")
        view_message = Permission.objects.get(codename="view_message")
        view_attempts = Permission.objects.get(codename="view_mailing_attempts")
        block_users = Permission.objects.get(codename="can_block_user")
        finish_mailing = Permission.objects.get(codename="can_finish_mailing")
        managers.permissions.add(
            view_users, view_mailing, view_recipient, block_users, finish_mailing, view_message, view_attempts
        )
