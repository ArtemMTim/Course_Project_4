from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from users.apps import UsersConfig

from .views import (
    BlockUserView,
    RegisterView,
    UnblockUserView,
    UserDetailView,
    UserForgotPasswordView,
    UserPasswordResetConfirmView,
    UsersListView,
    UserUpdateView,
    email_verification,
)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path(
        "register/",
        RegisterView.as_view(template_name="register.html"),
        name="register",
    ),
    path("email_confirm/<str:token>/", email_verification, name="email_verification"),
    path("password-reset/", UserForgotPasswordView.as_view(), name="password_reset"),
    path("set-new-password/<uidb64>/<token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("users_list/", cache_page(60)(UsersListView.as_view()), name="users_list"),
    path("users/<int:pk>/block", BlockUserView.as_view(), name="users_block"),
    path("users/<int:pk>/unblock", UnblockUserView.as_view(), name="users_unblock"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="users_detail"),
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="users_update"),
]
