from django.core.cache import cache

from mailing.models import Message, Recipient, Mailing, Mailing_Attempts
from config.settings import CACHE_ENABLED


def get_message_list():
    """Работает с кэш при просмотре всех сообщений.
    Записывает и достаёт из кэш."""
    if not CACHE_ENABLED:
        return Message.objects.all()
    else:
        key = "product_list"
        messages = cache.get(key)
        if messages is not None:
            return messages
        else:
            messages = Message.objects.all()
            cache.set(key, messages, 60)
            return messages



