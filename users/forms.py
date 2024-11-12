from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserCreationForm, UserChangeForm

from .models import User


class UserRegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False, help_text="Введите номер телефона")
    country = forms.CharField(max_length=50, required=False, help_text="Укажите Вашу страну проживания")

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "avatar",
            "country",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите адрес электронной почты"}
        )
        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите Ваше имя"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите Вашу фамилию"})
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите номер телефона"}
        )
        self.fields["avatar"].widget.attrs.update({"class": "form-control", "placeholder": "Загрузите Ваш аватар"})
        self.fields["country"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Укажите Вашу страну проживания"}
        )
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        return phone_number

class UserUpdateForm(UserChangeForm):
    phone_number = forms.CharField(max_length=15, required=False, help_text="Введите номер телефона")
    country = forms.CharField(max_length=50, required=False, help_text="Укажите Вашу страну проживания")

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "avatar",
            "country",

        ]

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите адрес электронной почты"}
        )
        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите Ваше имя"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите Вашу фамилию"})
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите номер телефона"}
        )
        self.fields["avatar"].widget.attrs.update({"class": "form-control", "placeholder": "Загрузите Ваш аватар"})
        self.fields["country"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Укажите Вашу страну проживания"}
        )


    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        return phone_number



################################################################


class UserForgotPasswordForm(PasswordResetForm):
    """
    Запрос на восстановление пароля
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class UserSetNewPasswordForm(SetPasswordForm):
    """
    Изменение пароля пользователя после подтверждения
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})
