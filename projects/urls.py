from django.urls import path

from projects.views import project_detail

urlpatterns = [
    path("projects/<int:project_id>/", project_detail, name="project_detail"),

]
