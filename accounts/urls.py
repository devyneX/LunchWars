"""URLs for the accounts app."""
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views


app_name = "accounts"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "login/",
        views.Login.as_view(),
        name="login",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change.html",
            success_url=reverse_lazy("accounts:password_change_done"),
        ),
        name="password_change",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
