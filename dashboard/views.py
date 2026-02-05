from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from projects.models import Project
from tasks.models import Task


@login_required
def dashboard(request):
    role = request.user.profile.role

    if role == "manager":
        projects = Project.objects.filter(created_by=request.user)
        return render(request, "dashboard/manager.html", {
            "projects": projects
        })

    if role == "member":
        tasks = Task.objects.filter(assigned_to=request.user)
        return render(request, "dashboard/member.html", {
            "tasks": tasks
        })

    # admin
    projects = Project.objects.all()
    return render(request, "dashboard/admin.html", {
        "projects": projects
    })
