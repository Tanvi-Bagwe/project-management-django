from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from accounts.models.profile import Profile


def register(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password'],
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', '')
        )

        Profile.objects.create(
            user=user,
            phone=request.POST.get('phone'),
            role=request.POST.get('role')
        )

        return redirect('register')

    return render(request, 'accounts/register.html')
