import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models.profile import Profile


# --- 1. LOGIN VALIDATOR ---
# Using a class to group credential checks keeps the login_submit view clean
class LoginValidator:
    @staticmethod
    def validate_credentials(username, password):
        if not username or not password:
            return "Username and password are required."
        return None


# --- 2. REGISTRATION VALIDATOR ---
# This acts as our "Logic Layer." It validates data before we touch the database.
class RegistrationValidator:
    @staticmethod
    def validate_names(f_name, l_name):
        if len(f_name) < 2 or len(l_name) < 2:
            return "Names must be at least 2 characters long."
        return None

    @staticmethod
    def validate_username_pattern(username):
        # Using Regex to ensure the username is 5-12 alphanumeric characters
        if not re.match(r'^[a-zA-Z0-9]{5,12}$', username):
            return "Username must be 5-12 characters and alphanumeric."
        return None

    @staticmethod
    def validate_email_pattern(email):
        # Basic regex check for a standard email format
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return "Invalid email format."
        return None

    @staticmethod
    def validate_password_strength(password):
        # Requirements: At least 8 chars, 1 letter, 1 number
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            return "Password must be at least 8 characters with a letter and a number."
        return None

    @staticmethod
    def check_existence(username, email):
        # Check the DB to make sure the user doesn't already exist
        if User.objects.filter(username=username).exists():
            return "Username already exists."
        if User.objects.filter(email=email).exists():
            return "Email already registered."
        return None


# --- 3. DATABASE SERVICE ---
@transaction.atomic
def create_user_account(data):
    """Handles the actual insertion into both the User and Profile tables"""
    # Create the standard Django user
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    # Create the custom Profile linked to that user
    Profile.objects.create(
        user=user,
        phone=data.get('phone'),
        role=data.get('role', 'member')  # Default to 'member' if none provided
    )
    return user


# --- 4. VIEWS (Request/Response) ---

def register(request):
    return render(request, 'accounts/register.html')


def login_page(request):
    # If already logged in, don't show the login page, just go to dashboard
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def register_submit(request):
    """Processes the AJAX registration form"""
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request"}, status=405)

    # Pulling data from the POST request
    data = {
        'first_name': request.POST.get('first_name', '').strip(),
        'last_name': request.POST.get('last_name', '').strip(),
        'username': request.POST.get('username', '').strip(),
        'email': request.POST.get('email', '').strip(),
        'password': request.POST.get('password', ''),
        'phone': request.POST.get('phone', ''),
        'role': request.POST.get('role', 'member')
    }

    # Modular Validation: We call each check one by one
    err = RegistrationValidator.validate_names(data['first_name'], data['last_name'])
    if err: return JsonResponse({"success": False, "message": err}, status=400)

    err = RegistrationValidator.validate_username_pattern(data['username'])
    if err: return JsonResponse({"success": False, "message": err}, status=400)

    err = RegistrationValidator.validate_email_pattern(data['email'])
    if err: return JsonResponse({"success": False, "message": err}, status=400)

    err = RegistrationValidator.validate_password_strength(data['password'])
    if err: return JsonResponse({"success": False, "message": err}, status=400)

    err = RegistrationValidator.check_existence(data['username'], data['email'])
    if err: return JsonResponse({"success": False, "message": err}, status=400)

    # If all checks pass, we create the account
    try:
        create_user_account(data)
        return JsonResponse({"success": True, "message": "Account created successfully!"})
    except Exception as e:
        return JsonResponse({"success": False, "message": "Could not create account."}, status=500)


def login_submit(request):
    """Processes the AJAX login form"""
    if request.user.is_authenticated:
        return JsonResponse({"success": True, "redirect_url": "/dashboard/"})

    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request"}, status=405)

    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "").strip()

    # Basic credential check
    err = LoginValidator.validate_credentials(username, password)
    if err:
        return JsonResponse({"success": False, "message": err}, status=400)

    # Check if the account is active/disabled before authenticating
    try:
        user_check = User.objects.get(username=username)
        if not user_check.is_active:
            return JsonResponse({
                "success": False,
                "message": "This account is disabled. Contact admin."
            }, status=403)
    except User.DoesNotExist:
        pass

    # Standard Django authentication
    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({"success": False, "message": "Invalid username or password"}, status=401)

    login(request, user)
    return JsonResponse({"success": True, "message": "Login successful!", "redirect_url": "/dashboard/"})


@login_required
def admin_users(request):
    # Only superusers should see the user list
    if not request.user.is_superuser:
        return render(request, "403.html")

    # select_related avoids the "N+1" problem by joining Profile to User
    users = User.objects.select_related("profile").all()
    return render(request, "accounts/users.html", {"users": users})


@login_required
def toggle_user(request, user_id):
    # Endpoint to enable or disable accounts from the admin panel
    if request.method != "POST" or not request.user.is_superuser:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()

    return JsonResponse({"success": True})
