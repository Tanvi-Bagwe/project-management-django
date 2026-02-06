from django.urls import path

from projects.views import project_detail, create_project, admin_projects, delete_project

urlpatterns = [
    path("projects/<int:project_id>/", project_detail, name="project_detail"),

    path("projects/create/", create_project, name="create_project"),

    path("projects/admin", admin_projects, name="admin_projects"),

    path('projects/<int:project_id>/delete/', delete_project, name='delete_project'),

]
