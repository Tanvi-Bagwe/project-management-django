from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from accounts.models.profile import Profile
from projects.models import Project
from tasks.models import Task


@login_required
def dashboard(request):
    role = request.user.profile.role

    if role == "admin":
        # 1. Get the counts first (more efficient)
        p_count = Project.objects.count()
        t_count = Task.objects.count()
        u_count = User.objects.count()
        m_mgr_count = Profile.objects.filter(role="manager").count()
        m_mem_count = Profile.objects.filter(role="member").count()

        # 2. Build the list for the template loop
        stats_list = [
            {"label": "Projects", "value": p_count, "icon": "folder", "color": "primary"},
            {"label": "Tasks", "value": t_count, "icon": "check2-square", "color": "success"},
            {"label": "Users", "value": u_count, "icon": "people", "color": "dark"},
            {"label": "Managers", "value": m_mgr_count, "icon": "person-badge", "color": "warning"},
            {"label": "Members", "value": m_mem_count, "icon": "person", "color": "info"},
        ]

        # 3. PASS AS A DICTIONARY
        return render(request, "dashboard/admin.html", {"stats": stats_list})

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

    return None
