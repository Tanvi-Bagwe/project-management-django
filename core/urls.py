import os
import smtplib
from email.message import EmailMessage

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import path, include


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(request, "landing.html")


def test_smtp(request):
    # 1. Pull the variables (Exactly how Django sees them)
    host = os.getenv('EMAIL_HOST')
    port = os.getenv('EMAIL_PORT')
    user = os.getenv('EMAIL_HOST_USER')
    password = os.getenv('EMAIL_HOST_PASSWORD')
    target_email = "tanvibagwe97@gmail.com"  # <--- Change to your email for the test

    output = []
    output.append("--- Environment Variable Check ---")
    output.append(f"HOST: {host}")
    output.append(f"PORT: {port}")
    output.append(f"USER: {user}")
    output.append(f"USER: {password}")
    output.append(f"PASSWORD: {'SET' if password else 'MISSING'}")

    if not all([host, port, user, password]):
        return HttpResponse("<br>".join(output) + "<br><b>ERROR: Missing variables!</b>")

    try:
        p_int = int(port)
        output.append(f"Connecting to {host}:{p_int}...")

        # Use SSL for 465, TLS for 587
        if p_int == 465:
            server = smtplib.SMTP_SSL(host, p_int, timeout=10)
        else:
            server = smtplib.SMTP(host, p_int, timeout=10)
            server.starttls()

        output.append("✅ Connection established.")

        server.login(user, password)
        output.append("✅ Login successful!")

        # Send test mail
        msg = EmailMessage()
        msg.set_content("Success! Your Railway email settings are working.")
        msg['Subject'] = "Railway SMTP Test"
        msg['From'] = user
        msg['To'] = target_email

        server.send_message(msg)
        output.append(f"✅ Email sent to {target_email}!")
        server.quit()

    except Exception as e:
        output.append(f"❌ FAILED: {str(e)}")

    # Join the list with HTML line breaks to show in browser
    return HttpResponse("<br>".join(output))


urlpatterns = [
    path("", root_redirect, name="landing"),
    path('', include('accounts.urls')),
    path('', include('dashboard.urls')),
    path('', include('tasks.urls')),
    path('', include('projects.urls')),
    path('', include('messaging.urls')),

    path("test-mail/", test_smtp),
]
