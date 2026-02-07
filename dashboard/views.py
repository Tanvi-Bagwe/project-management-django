from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from accounts.models.profile import Profile
from projects.models import Project
from tasks.models import Task


@login_required
def dashboard(request):
    # Get the user's role from their profile to decide which dashboard to show
    # I used getattr here just in case a user profile is missing a role
    role = getattr(request.user.profile, 'role', 'member')

    # ADMIN VIEW: Show high-level stats about the whole system
    if role == "admin":
        # Get counts of all main items in the database
        p_count = Project.objects.count()
        t_count = Task.objects.count()
        u_count = User.objects.count()

        # Count users based on their specific roles
        m_mgr_count = Profile.objects.filter(role="manager").count()
        m_mem_count = Profile.objects.filter(role="member").count()

        # Organize the stats into a list so the template can loop through them easily
        stats_list = [
            {"label": "Projects", "value": p_count, "icon": "folder", "color": "primary"},
            {"label": "Tasks", "value": t_count, "icon": "check2-square", "color": "success"},
            {"label": "Users", "value": u_count, "icon": "people", "color": "dark"},
            {"label": "Managers", "value": m_mgr_count, "icon": "person-badge", "color": "warning"},
            {"label": "Members", "value": m_mem_count, "icon": "person", "color": "info"},
        ]

        return render(request, "dashboard/admin.html", {"stats": stats_list})

    # MANAGER VIEW: Show projects that this manager created
    if role == "manager":
        # Only show projects belonging to the logged-in manager
        projects = Project.objects.filter(created_by=request.user).order_by('-id')
        return render(request, "dashboard/manager.html", {
            "projects": projects
        })

    # MEMBER VIEW: Show tasks specifically assigned to this user
    if role == "member":
        # select_related makes sure we get project/status info in one query
        tasks = Task.objects.filter(assigned_to=request.user).select_related('project', 'status')
        return render(request, "dashboard/member.html", {
            "tasks": tasks
        })

    # FALLBACK: If the role doesn't match anything, just show the member dashboard
    return render(request, "dashboard/member.html")
