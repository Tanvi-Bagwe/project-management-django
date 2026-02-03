from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from accounts.models.profile import Profile


def register(request):
    return render(request, 'accounts/register.html')


@csrf_exempt  # OK for AJAX during dev
def register_submit(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

    data = request.POST

    # Backend validations
    required_fields = ['username', 'email', 'password', 'first_name']
    for field in required_fields:
        if not data.get(field):
            return JsonResponse({
                "success": False,
                "message": f"{field.replace('_', ' ').title()} is required"
            }, status=400)

    if User.objects.filter(username=data['username']).exists():
        return JsonResponse({"success": False, "message": "Username already exists"}, status=400)

    if User.objects.filter(email=data['email']).exists():
        return JsonResponse({"success": False, "message": "Email already registered"}, status=400)

    # Create user
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data.get('last_name', '')
    )

    Profile.objects.create(
        user=user,
        phone=data.get('phone'),
        role=data.get('role', 'member')
    )

    return JsonResponse({
        "success": True,
        "message": "Registration successful! You can now login."
    })
