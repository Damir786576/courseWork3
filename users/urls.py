from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, PasswordRecoveryView, confirm_email

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("password_recovery/", PasswordRecoveryView.as_view(), name="password_recovery"),
    path("confirm/<str:token>/", confirm_email, name="confirm_email"),
]

