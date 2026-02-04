from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projects.models import Project
from tasks.models import Task


@login_required(login_url="login")
def dashboard(request):
    user = request.user

    projects = Project.objects.filter(
        id__in=Task.objects.filter(assigned_to=user)
        .values_list("project_id", flat=True)
        .distinct()
    )

    tasks = Task.objects.filter(assigned_to=user)

    context = {
        "projects": projects,
        "tasks": tasks
    }

    return render(request, "dashboard/index.html", context)
