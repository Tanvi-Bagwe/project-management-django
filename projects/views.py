from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
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


@login_required
def create_project(request):
    if request.user.profile.role != "manager":
        return JsonResponse({"error": "Unauthorized"}, status=403)

    if request.method == "POST":
        project = Project.objects.create(
            name=request.POST["name"],
            description=request.POST["description"],
            created_by=request.user,
            status_id=1  # active
        )
        return JsonResponse({
            "success": True,
            "project_id": project.id
        })
    return None
