from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

from projects.models import Project
from tasks.models import Task, TaskStatus, TaskPriority


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    tasks = Task.objects.filter(project_id=project_id)

    return render(request, "projects/detail.html", {
        "project": project,
        "tasks": tasks,
        "users": User.objects.filter(is_active=True),
        "statuses": TaskStatus.objects.all(),
        "priorities": TaskPriority.objects.all()
    })
