from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Task, TaskStatus


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
