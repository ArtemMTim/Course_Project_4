from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig

from .views import RegisterView, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path(
        "register/",
        RegisterView.as_view(template_name="register.html"),
        name="register",
    ),
    path('email_confirm/<str:token>/', email_verification, name="email_verification"),
]

################################################################
# urlpatterns = [
# path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
# path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
# ]
