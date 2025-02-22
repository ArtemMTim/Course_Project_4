# Generated by Django 5.1.2 on 2024-10-23 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="status",
            field=models.CharField(
                choices=[("создана", "создана"), ("запущена", "запущена"), ("завершена", "завершена")],
                default="создана",
                help_text="Введите статус рассылки",
                max_length=100,
                verbose_name="Статус рассылки",
            ),
        ),
        migrations.AlterField(
            model_name="mailing_attempts",
            name="attempt_status",
            field=models.CharField(
                choices=[("успешно", "успешно"), ("неуспешно", "неуспешно")],
                default="успешно",
                help_text="Введите статус",
                max_length=100,
                verbose_name="Статус попытки",
            ),
        ),
    ]
