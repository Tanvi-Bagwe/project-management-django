from django.contrib.auth import views as auth_views
from django.urls import path

from .views import register, register_submit, login_submit, login_page, logout_view, admin_users, toggle_user

urlpatterns = [
    path("register/", register, name="register"),
    path("register/submit/", register_submit, name="register_submit"),
    path("login/", login_page, name="login"),
    path("login/submit/", login_submit, name="login_submit"),
    path("logout/", logout_view, name="logout"),

    path("password-reset/",
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset.html"
         ),
         name="password_reset"),

    path("password-reset/done/",
         auth_views.PasswordResetDoneView.as_view(
             template_name="accounts/password_reset_done.html"
         ),
         name="password_reset_done"),

    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password_reset_confirm.html",
             success_url="/reset/done/"
         ),
         name="password_reset_confirm"),

    path("reset/done/",
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password_reset_complete.html"
         ),
         name="password_reset_complete"),

    path("users/", admin_users, name="admin_users"),

    path("users/<int:user_id>/toggle/", toggle_user, name="toggle_user"),
]
