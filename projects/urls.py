from django.urls import path

from projects.views import project_detail, create_project, admin_projects

urlpatterns = [
    path("projects/<int:project_id>/", project_detail, name="project_detail"),

    path("projects/create/", create_project, name="create_project"),

    path("projects/admin", admin_projects, name="admin_projects"),

]
