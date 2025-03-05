import secrets
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DetailView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, PasswordRecoveryForm
from .models import User
from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.token = secrets.token_hex(16)
        user.save()
        confirmation_link = f"http://127.0.0.1:8000/users/confirm/{user.token}/"
        send_mail(
            "Подтверждение регистрации",
            f"Перейдите по ссылке для подтверждения: {confirmation_link}",
            EMAIL_HOST_USER,
            [user.email],
        )
        return HttpResponse("Письмо с подтверждением отправлено на ваш email!")


def confirm_email(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None
    user.save()
    return redirect("home")


class PasswordRecoveryView(FormView):
    template_name = "users/password_recovery.html"
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.get(email=email)
        new_password = secrets.token_urlsafe(8)
        user.set_password(new_password)
        user.save()
        send_mail(
            "Восстановление пароля",
            f"Ваш новый пароль: {new_password}",
            EMAIL_HOST_USER,
            [email],
        )
        return HttpResponse("Новый пароль отправлен на ваш email.")


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile.html"
    context_object_name = "user"

    def get_object(self, **kwargs):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username", "email"]
    template_name = "users/profile_update.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, **kwargs):
        return self.request.user
