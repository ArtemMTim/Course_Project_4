from django.core.cache import cache

from config.settings import CACHE_ENABLED
from mailing.models import Mailing, Mailing_Attempts, Message, Recipient


def get_message_list():
    """Работает с кэш при просмотре всех сообщений.
    Записывает и достаёт из кэш."""
    if not CACHE_ENABLED:
        return Message.objects.all()
    else:
        key = "message_list"
        messages = cache.get(key)
        if messages is not None:
            return messages
        else:
            messages = Message.objects.all()
            cache.set(key, messages, 60)
            return messages


def get_recipient_list():
    """Работает с кэш при просмотре всех получателей.
    Записывает и достаёт из кэш."""
    if not CACHE_ENABLED:
        return Recipient.objects.all()
    else:
        key = "recipient_list"
        recipients = cache.get(key)
        if recipients is not None:
            return recipients
        else:
            recipients = Recipient.objects.all()
            cache.set(key, recipients, 60)
            return recipients


def get_mailing_list():
    """Работает с кэш при просмотре всех рассылок.
    Записывает и достаёт из кэш."""
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    else:
        key = "mailing_list"
        mailings = cache.get(key)
        if mailings is not None:
            return mailings
        else:
            mailings = Mailing.objects.all()
            cache.set(key, mailings, 60)
            return mailings


def get_mailing_attempts_list():
    """Работает с кэш при просмотре всех попыток отправки рассылок.
    Записывает и достаёт из кэш."""
    if not CACHE_ENABLED:
        return Mailing_Attempts.objects.all()
    else:
        key = "mailing_attempts_list"
        attempts = cache.get(key)
        if attempts is not None:
            return attempts
        else:
            attempts = Mailing_Attempts.objects.all()
            cache.set(key, attempts, 60)
            return attempts
