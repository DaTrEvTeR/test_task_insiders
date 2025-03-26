from . import views
from django.urls import path

app_name = "apps.users"

urlpatterns: list[path] = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("password_reset/", views.PasswordResetAPIView.as_view(), name="password_reset"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmAPIView.as_view(), name="password_reset_confirm"),
]
