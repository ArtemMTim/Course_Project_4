from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserForgotPasswordForm, UserRegisterForm, UserSetNewPasswordForm


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("mailing:main")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать!"
        message = "Ваша решистрация прошла успешно!"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, email_from, recipient_list)


#########


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """

    form_class = UserForgotPasswordForm
    template_name = "user_password_reset.html"
    success_url = reverse_lazy("login")
    success_message = "Письмо с инструкцией по восстановлению пароля отправлена на ваш email"
    subject_template_name = "registeruser/email/password_subject_reset_mail.txt"
    email_template_name = "registeruser/email/password_reset_mail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Запрос на восстановление пароля"
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """

    form_class = UserSetNewPasswordForm
    template_name = "registeruser/user_password_set_new.html"
    success_url = reverse_lazy("login")
    success_message = "Пароль успешно изменен. Можете авторизоваться на сайте."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Установить новый пароль"
        return context


# Create your views here.
