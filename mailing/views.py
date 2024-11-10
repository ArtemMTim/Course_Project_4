from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect


from .forms import MailingForm, MessageForm, RecipientForm
from .models import Mailing, Mailing_Attempts, Message, Recipient
from users.models import User


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

    def form_valid(self, form):
        recipients = form.save()
        user = self.request.user
        recipients.owner = user
        recipients.save()
        return super().form_valid(form)


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

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mailing_created"] = Mailing.objects.filter(status=Mailing.CREATED)
        context["mailing_active"] = Mailing.objects.filter(status=Mailing.ACTIVE)
        context["mailing_finished"] = Mailing.objects.filter(status=Mailing.FINISHED)
        return context


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"


class MailingCreateView(CreateView):
    model = Mailing
    # fields = ["start_at", "end_at", "status", "message", "recipients"]
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


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
        owner = mailing.owner
        recipient_list = [recipient.email for recipient in mailing.recipients.all()]

        try:
            send_mail(subject, message, email_from, recipient_list)
            mailing_attempts = Mailing_Attempts(
                attempt_date=datetime.now(),
                attempt_status=Mailing_Attempts.SUCCESS,
                mail_server_response="Email sent successfully",
                mailing=mailing,
                owner=owner,
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
                owner=owner,
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
    owner = mail.owner
    recipient_list = [recipient.email for recipient in mail.recipients.all()]

    try:
        send_mail(subject, message, email_from, recipient_list)
        mailing_attempts = Mailing_Attempts(
            attempt_date=datetime.now(),
            attempt_status=Mailing_Attempts.SUCCESS,
            mail_server_response="Email sent successfully",
            mailing=mail,
            owner=owner,
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
            owner=owner,
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
        owner = mailing.owner
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
                owner=owner,
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
                owner=owner,
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
    owner = mail.owner
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
            owner=owner,
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
            owner=owner,
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


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users_list.html"

class BlockUserView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if not request.user.has_perm("can_block_user"):
            return HttpResponseForbidden("У вас нет прав на это действие.")

        user.is_active = False
        user.save()
        return redirect("mailing:users_list")

class UnblockUserView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if not request.user.has_perm("can_block_user"):
            return HttpResponseForbidden("У вас нет прав на это действие.")

        user.is_active = True
        user.save()
        return redirect("mailing:users_list")