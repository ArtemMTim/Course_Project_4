from django.db import models


class Recipient(models.Model):
    email = models.EmailField(
        unique=True, verbose_name="Адрес электронной почты", help_text="Введите адрес электронной почты получателя"
    )
    full_name = models.CharField(
        max_length=255, verbose_name="Ф.И.О. получателя", help_text="Введите Ф.И.О. получателя"
    )
    comment = models.TextField(
        verbose_name="Комментарий", blank=True, null=True, help_text="Введите комментарий к получателю"
    )

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    class Meta:
        verbose_name = "получатель"
        verbose_name_plural = "получатели"
        ordering = ["full_name"]


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name="Тема сообщения", help_text="Введите тему сообщения")
    text = models.TextField(verbose_name="Текст сообщения", help_text="Введите текст сообщения")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ["subject"]


class Mailing(models.Model):
    FINISHED = "завершена"
    CREATED = "создана"
    ACTIVE = "запущена"
    STATUS_CHOICES = [(CREATED, "создана"), (ACTIVE, "запущена"), (FINISHED, "завершена")]
    start_at = models.DateTimeField(verbose_name="Начало рассылки", null=True, blank=True)
    end_at = models.DateTimeField(
        verbose_name="Окончание рассылки", help_text="Введите дату и время окончания рассылки", null=True, blank=True
    )
    status = models.CharField(
        max_length=100,
        verbose_name="Статус рассылки",
        help_text="Введите статус рассылки",
        choices=STATUS_CHOICES,
        default=CREATED,
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение", help_text="Выберите сообщение для рассылки"
    )
    recipients = models.ManyToManyField(
        Recipient, verbose_name="Получатели", help_text="Выберите получателей для рассылки"
    )

    def __str__(self):
        return f"{self.message.subject} - {self.status}"

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ["status", "message"]


class Mailing_Attempts(models.Model):
    SUCCESS = "успешно"
    FAILURE = "неуспешно"
    ATTEMPT_STATUS_CHOICES = [(SUCCESS, "успешно"), (FAILURE, "неуспешно")]
    attempt_date = models.DateTimeField(verbose_name="Дата попытки", help_text="Введите дату и время попытки")
    attempt_status = models.CharField(
        max_length=100,
        verbose_name="Статус попытки",
        help_text="Введите статус",
        choices=ATTEMPT_STATUS_CHOICES,
        default=SUCCESS,
    )
    mail_server_response = models.TextField(
        verbose_name="Ответ сервера почты", help_text="Введите ответ сервера почты"
    )
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка", help_text="Выберите рассылку для попытки"
    )

    def __str__(self):
        return f"{self.mailing.message.subject} - {self.attempt_status} - {self.mail_server_response} - {self.attempt_date}"

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылки"
        ordering = ["attempt_status", "mailing"]


# Create your models here.
