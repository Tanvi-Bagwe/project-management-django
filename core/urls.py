from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('dashboard.urls')),
    path('', include('tasks.urls')),
    path('', include('projects.urls')),
    path('', include('messaging.urls')),
]
