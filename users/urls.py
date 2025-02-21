from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, confirm_email, PasswordRecoveryView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("confirm/<str:token>/", confirm_email, name="confirm_email"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="users:login"), name="logout"),
    path("password-recovery/", PasswordRecoveryView.as_view(), name="password_recovery"),
]

