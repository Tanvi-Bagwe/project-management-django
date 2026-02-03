from django.urls import path

from .views import register, register_submit

urlpatterns = [
    path("register/", register, name="register"),
    path("register/submit/", register_submit, name="register_submit"),
]
