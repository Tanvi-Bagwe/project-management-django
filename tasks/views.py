import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now

from projects.models import Project
from .models import Task, TaskStatus, TaskPriority

logger = logging.getLogger(__name__)


@login_required
def task_detail(request, task_id):
    """
    VIEW: Task Detail
    Purpose: Displays individual task information.
    Includes a security check to ensure only the assigned user can view the details.
    """
    task = get_object_or_404(Task, id=task_id)

    # ACCESS CONTROL: Prevent users from 'ID guessing' tasks not assigned to them
    if task.assigned_to != request.user:
        return render(request, "403.html")

    statuses = TaskStatus.objects.all()

    return render(request, "tasks/detail.html", {
        "task": task,
        "statuses": statuses
    })


@login_required
def update_task_status(request, task_id):
    """
    API ENDPOINT: Update Task Status
    Purpose: Handles AJAX POST requests to update the status of a task in real-time.
    """
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)

        # SECURITY: Only the person responsible for the task can update its status
        if task.assigned_to != request.user:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        status_id = request.POST.get("status_id")
        task.status_id = status_id
        task.save()  # Commit change to Database

        return JsonResponse({"success": True})

    # Return 405 if someone tries to 'GET' this URL
    return JsonResponse({"error": "Method not allowed"}, status=405)


@login_required
def create_task(request):
    """
    VIEW & API: Create Task
    Purpose: GET requests return the creation form; POST requests process the AJAX form data.
    Restricted to users with the 'manager' role.
    """
    # ROLE-BASED ACCESS CONTROL (RBAC)
    if request.user.profile.role != "manager":
        return JsonResponse({"error": "Only managers can create tasks"}, status=403)

    if request.method == "POST":
        # DATA CLEANING: strip() removes accidental whitespace from user input
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        project_id = request.POST.get("project_id")

        # BACKEND VALIDATION: Ensures integrity even if JS validation is bypassed
        if not title or not description or not project_id:
            return JsonResponse({
                "success": False,
                "message": "Title, Description, and Project are required."
            }, status=400)

        assigned_to = request.POST.get("assigned_to")
        status_id = request.POST.get("status_id")
        priority_id = request.POST.get("priority_id")

        if not all([assigned_to, status_id, priority_id]):
            return JsonResponse({"success": False, "message": "Missing required selection fields."}, status=400)

        # OBJECT CREATION: Maps POST data to Database Model fields
        Task.objects.create(
            project_id=project_id,
            title=title,
            description=description,
            assigned_to_id=assigned_to,
            assigned_by=request.user,
            status_id=status_id,
            priority_id=priority_id,
            due_date=request.POST.get("due_date") or None,
            assigned_at=now()
        )
        return JsonResponse({"success": True})

    # Context for the GET request (Populating dropdowns)
    return render(request, "tasks/create.html", {
        "projects": Project.objects.all(),
        # Optimization: Only show active team members in the assignee dropdown
        "users": User.objects.filter(is_active=True, profile__role="member"),
        "statuses": TaskStatus.objects.all(),
        "priorities": TaskPriority.objects.all()
    })


@login_required
def delete_task(request, task_id):
    """
    API ENDPOINT: Delete Task
    Purpose: Implements a RESTful DELETE handler to remove tasks from the system.
    Strictly restricted to 'manager' users.
    """
    if request.method != "DELETE":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    task = get_object_or_404(Task, id=task_id)

    # ROLE CHECK: Verify user permissions before deletion
    if request.user.profile.role != "manager":
        return JsonResponse({"error": "Unauthorized"}, status=403)

    logger.info(f"User {request.user.username} (ID: {request.user.id}) is deleting Task: {task.title}")
    
    task.delete()
    return JsonResponse({"success": True})
