from django import forms
from django.core.exceptions import ValidationError

from .models import Mailing, Mailing_Attempts, Message, Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ("email", "full_name", "comment")

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите адрес электронной почты"}
        )
        self.fields["full_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите полное имя"})
        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Введите комментарий"})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Recipient.objects.filter(email=email).exists():
            raise ValidationError("Такой адрес электронной почты уже существует в БД!")
        return email


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("subject", "text")

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields["subject"].widget.attrs.update({"class": "form-control", "placeholder": "Введите тему сообщения"})
        self.fields["text"].widget.attrs.update({"class": "form-control", "placeholder": "Введите текст сообщения"})


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ("start_at", "end_at", "status", "message", "recipients")

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields["start_at"].widget.attrs.update({"class": "form-control", "type": "datetime-local"})
        self.fields["end_at"].widget.attrs.update({"class": "form-control", "type": "datetime-local"})
        self.fields["recipients"].widget.attrs.update({"class": "form-control"})
        self.fields["status"].widget.attrs.update({"class": "form-control"})
        self.fields["message"].widget.attrs.update({"class": "form-control"})
