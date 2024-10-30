from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import MailingForm, MessageForm, RecipientForm
from .models import Mailing, Mailing_Attempts, Message, Recipient


class MailingView(TemplateView):
    models = [Recipient, Mailing]
    template_name = "mailing/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipients_all"] = Recipient.objects.all()
        context["mailing_all"] = Mailing.objects.all()
        context["mailing_active"] = Mailing.objects.filter(status=Mailing.ACTIVE)
        return context


class RecipientListView(ListView):
    model = Recipient
    template_name = "mailing/recipient_list.html"


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = "mailing/recipient_detail.html"


class RecipientCreateView(CreateView):
    model = Recipient
    # fields = ["email", "full_name", "comment"]
    form_class = RecipientForm
    template_name = "mailing/recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientUpdateView(UpdateView):
    model = Recipient
    # fields = ["email", "full_name", "comment"]
    form_class = RecipientForm
    template_name = "mailing/recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def get_success_url(self):
        return reverse_lazy("mailing:recipient_detail", kwargs={"pk": self.object.pk})


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "mailing/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailing:recipient_list")


class MessageListView(ListView):
    model = Message
    template_name = "mailing/message_list.html"


class MessageDetailView(DetailView):
    model = Message
    template_name = "mailing/message_detail.html"


class MessageCreateView(CreateView):
    model = Message
    # fields = ["subject", "text"]
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    # fields = ["subject", "text"]
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_success_url(self):
        return reverse_lazy("mailing:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"


class MailingCreateView(CreateView):
    model = Mailing
    # fields = ["start_at", "end_at", "status", "message", "recipients"]
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    # fields = ["start_at", "end_at", "status", "message", "recipients"]
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")


class MailingAttemptsListView(ListView):
    model = Mailing_Attempts
    template_name = "mailing/mailing_attempts_list.html"


def sending_mail_active(request, *args, **kwargs):
    mails = Mailing.objects.filter(status=Mailing.ACTIVE)
    email_from = settings.EMAIL_HOST_USER
    attempts_list = []

    for mailing in mails:
        subject = mailing.message.subject
        message = mailing.message.text
        recipient_list = [recipient.email for recipient in mailing.recipients.all()]

        try:
            send_mail(subject, message, email_from, recipient_list)
            mailing_attempts = Mailing_Attempts(
                attempt_date=datetime.now(),
                attempt_status=Mailing_Attempts.SUCCESS,
                mail_server_response="Email sent successfully",
                mailing=mailing,
            )
            mailing_attempts.save()
            result = "Sending mail successful"

            attempts_list.append((result, subject, message, recipient_list))

        except Exception as e:
            mailing_attempts = Mailing_Attempts(
                attempt_date=datetime.now(),
                attempt_status=Mailing_Attempts.FAILURE,
                mail_server_response=str(e),
                mailing=mailing,
            )
            mailing_attempts.save()
            result = f"Sending mail failed with: {str(e)}"

            attempts_list.append((result, subject, message, recipient_list))

    context = {"attempts_list": attempts_list}
    return render(request, "mailing/send_mail_result.html", context)


def sending_one_mail_active(request, pk):
    mail = Mailing.objects.get(pk=pk)

    email_from = settings.EMAIL_HOST_USER
    attempts_list = []

    subject = mail.message.subject
    message = mail.message.text
    recipient_list = [recipient.email for recipient in mail.recipients.all()]

    try:
        send_mail(subject, message, email_from, recipient_list)
        mailing_attempts = Mailing_Attempts(
            attempt_date=datetime.now(),
            attempt_status=Mailing_Attempts.SUCCESS,
            mail_server_response="Email sent successfully",
            mailing=mail,
        )
        mailing_attempts.save()
        result = "Sending mail successful"

        attempts_list.append((result, subject, message, recipient_list))

    except Exception as e:
        mailing_attempts = Mailing_Attempts(
            attempt_date=datetime.now(),
            attempt_status=Mailing_Attempts.FAILURE,
            mail_server_response=str(e),
            mailing=mail,
        )
        mailing_attempts.save()
        result = f"Sending mail failed with: {str(e)}"

        attempts_list.append((result, subject, message, recipient_list))

    context = {"attempts_list": attempts_list}
    return render(request, "mailing/send_mail_result.html", context)


def sending_mail_created(request, *args, **kwargs):
    mails = Mailing.objects.filter(status=Mailing.CREATED)
    email_from = settings.EMAIL_HOST_USER
    attempts_list = []

    for mailing in mails:
        subject = mailing.message.subject
        message = mailing.message.text
        recipient_list = [recipient.email for recipient in mailing.recipients.all()]

        try:
            send_mail(subject, message, email_from, recipient_list)
            mailing.status = Mailing.ACTIVE
            mailing.start_at = datetime.now()
            mailing.save()
            mailing_attempts = Mailing_Attempts(
                attempt_date=datetime.now(),
                attempt_status=Mailing_Attempts.SUCCESS,
                mail_server_response="Email sent successfully",
                mailing=mailing,
            )
            mailing_attempts.save()
            result = "Sending mail successful"
            attempts_list.append((result, subject, message, recipient_list))

        except Exception as e:
            mailing.status = Mailing.ACTIVE
            mailing.start_at = datetime.now()
            mailing.save()
            mailing_attempts = Mailing_Attempts(
                attempt_date=datetime.now(),
                attempt_status=Mailing_Attempts.FAILURE,
                mail_server_response=str(e),
                mailing=mailing,
            )
            mailing_attempts.save()
            result = f"Sending mail failed with: {str(e)}"
            attempts_list.append((result, subject, message, recipient_list))

    context = {"attempts_list": attempts_list}
    return render(request, "mailing/send_mail_result.html", context)


def sending_one_mail_created(request, pk):
    mail = Mailing.objects.get(pk=pk)

    email_from = settings.EMAIL_HOST_USER
    attempts_list = []

    subject = mail.message.subject
    message = mail.message.text
    recipient_list = [recipient.email for recipient in mail.recipients.all()]

    try:
        send_mail(subject, message, email_from, recipient_list)
        mail.status = Mailing.ACTIVE
        mail.start_at = datetime.now()
        mail.save()
        mailing_attempts = Mailing_Attempts(
            attempt_date=datetime.now(),
            attempt_status=Mailing_Attempts.SUCCESS,
            mail_server_response="Email sent successfully",
            mailing=mail,
        )
        mailing_attempts.save()
        result = "Sending mail successful"
        attempts_list.append((result, subject, message, recipient_list))

    except Exception as e:
        mail.status = Mailing.ACTIVE
        mail.start_at = datetime.now()
        mail.save()
        mailing_attempts = Mailing_Attempts(
            attempt_date=datetime.now(),
            attempt_status=Mailing_Attempts.FAILURE,
            mail_server_response=str(e),
            mailing=mail,
        )
        mailing_attempts.save()
        result = f"Sending mail failed with: {str(e)}"
        attempts_list.append((result, subject, message, recipient_list))

    context = {"attempts_list": attempts_list}
    return render(request, "mailing/send_mail_result.html", context)


def finish_mailing(request, pk):
    mail = Mailing.objects.get(pk=pk)
    mail.status = Mailing.FINISHED
    mail.end_at = datetime.now()
    mail.save()
    context = {"mail": mail}
    return render(request, "mailing/finished_mailing_info.html", context)
