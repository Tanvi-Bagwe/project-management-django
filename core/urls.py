from django.shortcuts import redirect
from django.urls import path, include


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


urlpatterns = [
    path('', root_redirect),
    path('', include('accounts.urls')),
    path('', include('dashboard.urls')),
    path('', include('tasks.urls')),
    path('', include('projects.urls')),
    path('', include('messaging.urls')),
]
