from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models.profile import Profile


@login_required(login_url="login")
def dashboard(request):
    profile = Profile.objects.get(user=request.user)

    context = {
        "role": profile.role
    }

    return render(request, "dashboard/index.html", context)
