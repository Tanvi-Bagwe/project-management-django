from django.shortcuts import redirect, render
from django.urls import path, include


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(request, "landing.html")


urlpatterns = [
    path("", root_redirect, name="landing"),
    path('', include('accounts.urls')),
    path('', include('dashboard.urls')),
    path('', include('tasks.urls')),
    path('', include('projects.urls')),
    path('', include('messaging.urls')),
]
