from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now

from projects.models import Project
from .models import Task, TaskStatus, TaskPriority


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # security check
    if task.assigned_to != request.user:
        return render(request, "403.html")

    statuses = TaskStatus.objects.all()

    return render(request, "tasks/detail.html", {
        "task": task,
        "statuses": statuses
    })


@login_required
def update_task_status(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)

        if task.assigned_to != request.user:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        status_id = request.POST.get("status_id")
        task.status_id = status_id
        task.save()

        return JsonResponse({"success": True})
    return None


@login_required
def create_task(request):
    if request.user.profile.role != "manager":
        return JsonResponse({"error": "Unauthorized"}, status=403)

    if request.method == "POST":
        Task.objects.create(
            project_id=request.POST["project_id"],
            title=request.POST["title"],
            description=request.POST["description"],
            assigned_to_id=request.POST["assigned_to"],
            assigned_by=request.user,
            status_id=request.POST["status_id"],
            priority_id=request.POST["priority_id"],
            assigned_at=now()
        )
        return JsonResponse({"success": True})

    return render(request, "tasks/create.html", {
        "projects": Project.objects.all(),
        "users": User.objects.filter(is_active=True),
        "statuses": TaskStatus.objects.all(),
        "priorities": TaskPriority.objects.all()
    })


@login_required
def delete_task(request, task_id):
    if request.method != "DELETE":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405
        )

    task = get_object_or_404(Task, id=task_id)

    # Only manager can delete
    if request.user.profile.role != "manager":
        return JsonResponse(
            {"error": "Unauthorized"},
            status=403
        )

    task.delete()
    return JsonResponse({"success": True})
