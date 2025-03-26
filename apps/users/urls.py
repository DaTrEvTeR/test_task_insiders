from . import views
from django.urls import path

app_name = "apps.users"

urlpatterns: list[path] = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
]
