from django.urls import path

from .views import task_detail, update_task_status, create_task, delete_task

urlpatterns = [
    path("tasks/<int:task_id>/", task_detail, name="task_detail"),
    path("tasks/<int:task_id>/status/", update_task_status, name="task_status_update"),

    path("tasks/create/", create_task, name="create_task"),

    path("tasks/delete/<int:task_id>/", delete_task, name="delete_task"),

]
