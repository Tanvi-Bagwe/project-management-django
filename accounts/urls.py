from django.urls import path

from .views import register, register_submit, login_submit, login_page, logout_view

urlpatterns = [
    path("register/", register, name="register"),
    path("register/submit/", register_submit, name="register_submit"),
    path("login/", login_page, name="login"),
    path("login/submit/", login_submit, name="login_submit"),
    path("logout/", logout_view, name="logout"),
]
