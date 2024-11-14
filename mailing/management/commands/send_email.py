from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        subject = input("Введите тему письма: ")
        message = input("Введите текст письма: ")
        recipient = input("Введите адрес получателя: ")
        recipient_list = [recipient]
        email_from = settings.EMAIL_HOST_USER
        try:
            send_mail(subject, message, email_from, recipient_list)
            print("Письмо отправлено")
        except Exception as e:
            print(f"Ошибка при отправке письма: {str(e)}")
