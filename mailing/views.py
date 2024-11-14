from datetime import datetime

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from users.forms import UserUpdateForm
from users.models import User

from .forms import MailingForm, MessageForm, RecipientForm
from .models import Mailing, Mailing_Attempts, Message, Recipient
from .service import get_mailing_attempts_list, get_mailing_list, get_message_list, get_recipient_list


class UserDetailView(DetailView):
    model = User
    template_name = "user_detail.html"


class UserUpdateView(UpdateView):
    model = User
    # fields = ["email", "first_name", "last_name", "phone_number", "avatar", "country", ""]
    form_class = UserUpdateForm
    template_name = "users_form.html"
    success_url = reverse_lazy("mailing:main")


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
    """Контроллер отображения списка получателей."""

    model = Recipient
    template_name = "mailing/recipient_list.html"

    def get_queryset(self):
        if self.request.user.has_perm("view_recipient"):
            return get_recipient_list()

        return get_recipient_list().filter(owner=self.request.user)


class RecipientDetailView(DetailView):
    """Контроллер отображения подробностей о получателе."""

    model = Recipient
    template_name = "mailing/recipient_detail.html"


class RecipientCreateView(CreateView):
    """Контроллер создания получателя."""

    model = Recipient
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
    """Контроллер изменения получателя."""

    model = Recipient
    form_class = RecipientForm
    template_name = "mailing/recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def get_success_url(self):
        return reverse_lazy("mailing:recipient_detail", kwargs={"pk": self.object.pk})


class RecipientDeleteView(DeleteView):
    """Контроллер контроллер удаления получателя."""

    model = Recipient
    template_name = "mailing/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailing:recipient_list")


class MessageListView(ListView):
    """Контроллер отображения списка сообщений."""

    model = Message
    template_name = "mailing/message_list.html"

    def get_queryset(self):
        if self.request.user.has_perm("view_message"):
            return get_message_list()
        return get_message_list().filter(owner=self.request.user)


class MessageDetailView(DetailView):
    """Контроллер отображения подробностей о сообщении."""

    model = Message
    template_name = "mailing/message_detail.html"


class MessageCreateView(CreateView):
    """Контроллер создания сообщения."""

    model = Message
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
    """Контроллер изменения сообщения."""

    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_success_url(self):
        return reverse_lazy("mailing:message_detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(DeleteView):
    """Контроллер удаления сообщения."""

    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")


class MailingListView(ListView):
    """Контроллер отображения списка рассылок."""

    model = Mailing
    template_name = "mailing/mailing_list.html"

    def get_queryset(self):
        if self.request.user.has_perm("view_mailing"):
            return get_mailing_list()
        return get_mailing_list().filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing = self.get_queryset()
        context["mailing_created"] = mailing.filter(status=Mailing.CREATED)
        context["mailing_active"] = mailing.filter(status=Mailing.ACTIVE)
        context["mailing_finished"] = mailing.filter(status=Mailing.FINISHED)
        return context


class MailingDetailView(DetailView):
    """Контроллер отображения подробностей о рассылке."""

    model = Mailing
    template_name = "mailing/mailing_detail.html"


class MailingCreateView(CreateView):
    """Контроллер создания рассылки."""

    model = Mailing
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
    """Контроллер изменения рассылки."""

    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})


class MailingDeleteView(DeleteView):
    """Контроллер удаления рассылки."""

    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")


class MailingAttemptsListView(ListView):
    """Контроллер отображения списка попыток отправки."""

    model = Mailing_Attempts
    template_name = "mailing/mailing_attempts_list.html"

    def get_queryset(self):
        return get_mailing_attempts_list().filter(owner=self.request.user)


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
