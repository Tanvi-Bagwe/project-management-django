import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from accounts.models.profile import Profile


# --- LOGIN VALIDATOR ---

class LoginValidator:

    @staticmethod
    def validate_credentials(username, password):
        if not username or not password:
            return "Username and password are required."
        return None


# --- 1. VALIDATION SERVICE (Logic Layer) ---
class RegistrationValidator:

    @staticmethod
    def validate_names(f_name, l_name):
        if len(f_name) < 2 or len(l_name) < 2:
            return "Names must be at least 2 characters long."
        return None

    @staticmethod
    def validate_username_pattern(username):
        # 5-12 chars, alphanumeric
        if not re.match(r'^[a-zA-Z0-9]{5,12}$', username):
            return "Username must be 5-12 characters and alphanumeric."
        return None

    @staticmethod
    def validate_email_pattern(email):
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return "Invalid email format."
        return None

    @staticmethod
    def validate_password_strength(password):
        # Min 8 chars, 1 letter, 1 number
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            return "Password must be at least 8 characters with a letter and a number."
        return None

    @staticmethod
    def check_existence(username, email):
        if User.objects.filter(username=username).exists():
            return "Username already exists."
        if User.objects.filter(email=email).exists():
            return "Email already registered."
        return None


# --- 2. DATABASE SERVICE (Data Layer) ---
def create_user_account(data):
    """Handles the actual insertion into the DB"""
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    Profile.objects.create(
        user=user,
        phone=data.get('phone'),
        role=data.get('role', data['role'])
    )
    return user


# --- 3. THE VIEW (Request/Response Layer) ---

def register(request):
    return render(request, 'accounts/register.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@csrf_exempt
def register_submit(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request"}, status=405)

    # Extracting data
    data = {
        'first_name': request.POST.get('first_name', '').strip(),
        'last_name': request.POST.get('last_name', '').strip(),
        'username': request.POST.get('username', '').strip(),
        'email': request.POST.get('email', '').strip(),
        'password': request.POST.get('password', ''),
        'phone': request.POST.get('phone', ''),
        'role': request.POST.get('role', '')
    }

    # SEPARATE METHOD CALLS FOR EACH VALIDATION
    # This fulfills your "modular" requirement perfectly

    # Check Names
    err = RegistrationValidator.validate_names(data['first_name'], data['last_name'])
    if err: return JsonResponse({"success": False, "message": err}, status=400)

    # Check Username
    err = RegistrationValidator.validate_username_pattern(data['username'])
    if err: return JsonResponse({"success": False, "message": err}, status=400)

    # Check Email
    err = RegistrationValidator.validate_email_pattern(data['email'])
    if err: return JsonResponse({"success": False, "message": err}, status=400)

    # Check Password
    err = RegistrationValidator.validate_password_strength(data['password'])
    if err: return JsonResponse({"success": False, "message": err}, status=400)

    # Check DB Existence
    err = RegistrationValidator.check_existence(data['username'], data['email'])
    if err: return JsonResponse({"success": False, "message": err}, status=400)

    # If all modular checks pass, proceed to creation
    try:
        create_user_account(data)
        return JsonResponse({"success": True, "message": "Account created successfully!"})
    except Exception as e:
        return JsonResponse({"success": False, "message": "Database error occurred."}, status=500)


@csrf_exempt
def login_submit(request):
    if request.user.is_authenticated:
        return JsonResponse({
            "success": True,
            "message": "Already logged in",
            "redirect_url": "/dashboard/"
        })

    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request"}, status=405)

    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "").strip()

    err = LoginValidator.validate_credentials(username, password)
    if err:
        return JsonResponse({"success": False, "message": err}, status=400)

    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({"success": False, "message": "Invalid username or password"}, status=401)

    login(request, user)

    return JsonResponse({
        "success": True,
        "message": "Login successful!",
        "redirect_url": "/dashboard/"
    })
