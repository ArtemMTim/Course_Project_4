# Generated by Django 5.1.2 on 2024-10-22 12:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Mailing",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "start_at",
                    models.DateTimeField(
                        help_text="Введите дату и время начала рассылки", verbose_name="Начало рассылки"
                    ),
                ),
                (
                    "end_at",
                    models.DateTimeField(
                        help_text="Введите дату и время окончания рассылки", verbose_name="Окончание рассылки"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        help_text="Введите статус рассылки", max_length=100, verbose_name="Статус рассылки"
                    ),
                ),
            ],
            options={
                "verbose_name": "рассылка",
                "verbose_name_plural": "рассылки",
                "ordering": ["status", "message"],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "subject",
                    models.CharField(
                        help_text="Введите тему сообщения", max_length=100, verbose_name="Тема сообщения"
                    ),
                ),
                ("text", models.TextField(help_text="Введите текст сообщения", verbose_name="Текст сообщения")),
            ],
            options={
                "verbose_name": "сообщение",
                "verbose_name_plural": "сообщения",
                "ordering": ["subject"],
            },
        ),
        migrations.CreateModel(
            name="Recipient",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "email",
                    models.EmailField(
                        help_text="Введите адрес электронной почты получателя",
                        max_length=254,
                        unique=True,
                        verbose_name="Адрес электронной почты",
                    ),
                ),
                (
                    "full_name",
                    models.CharField(
                        help_text="Введите Ф.И.О. получателя", max_length=255, verbose_name="Ф.И.О. получателя"
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True, help_text="Введите комментарий к получателю", null=True, verbose_name="Комментарий"
                    ),
                ),
            ],
            options={
                "verbose_name": "получатель",
                "verbose_name_plural": "получатели",
                "ordering": ["full_name"],
            },
        ),
        migrations.CreateModel(
            name="Mailing_Attempts",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "attempt_date",
                    models.DateTimeField(help_text="Введите дату и время попытки", verbose_name="Дата попытки"),
                ),
                (
                    "attempt_status",
                    models.CharField(help_text="Введите статус", max_length=100, verbose_name="Статус попытки"),
                ),
                (
                    "mail_server_response",
                    models.TextField(help_text="Введите ответ сервера почты", verbose_name="Ответ сервера почты"),
                ),
                (
                    "mailing",
                    models.ForeignKey(
                        help_text="Выберите рассылку для попытки",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mailing.mailing",
                        verbose_name="Рассылка",
                    ),
                ),
            ],
            options={
                "verbose_name": "попытка рассылки",
                "verbose_name_plural": "попытки рассылки",
                "ordering": ["attempt_status", "mailing"],
            },
        ),
        migrations.AddField(
            model_name="mailing",
            name="message",
            field=models.ForeignKey(
                help_text="Выберите сообщение для рассылки",
                on_delete=django.db.models.deletion.CASCADE,
                to="mailing.message",
                verbose_name="Сообщение",
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="recipients",
            field=models.ManyToManyField(
                help_text="Выберите получателей для рассылки", to="mailing.recipient", verbose_name="Получатели"
            ),
        ),
    ]
