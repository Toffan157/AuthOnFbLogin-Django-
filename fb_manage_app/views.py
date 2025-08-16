from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
import requests

def login_view(request):
    fb_login_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth?"
        f"client_id={settings.FACEBOOK_CLIENT_ID}"
        f"&redirect_uri={settings.FACEBOOK_REDIRECT_URI}"
        f"&scope=email"
    )
    return render(request, "login.html", {"fb_login_url": fb_login_url})

def facebook_callback(request):
    code = request.GET.get("code")
    if not code:
        return redirect("login")

    # Step 1: Exchange code for access token
    token_url = (
        f"https://graph.facebook.com/v18.0/oauth/access_token?"
        f"client_id={settings.FACEBOOK_CLIENT_ID}"
        f"&redirect_uri={settings.FACEBOOK_REDIRECT_URI}"
        f"&client_secret={settings.FACEBOOK_CLIENT_SECRET}"
        f"&code={code}"
    )
    token_response = requests.get(token_url).json()
    access_token = token_response.get("access_token")

    if not access_token:
        return redirect("login")

    # Step 2: Get user info
    user_info_url = f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"
    user_info = requests.get(user_info_url).json()

    email = user_info.get("email", f"{user_info['id']}@facebook.com")
    name = user_info.get("name", "Facebook User")

    # Step 3: Create or get Django user
    user, _ = User.objects.get_or_create(username=email, defaults={"first_name": name})
    login(request, user)

    return redirect("home")

def home_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "home.html", {"user": request.user})

def logout_view(request):
    logout(request)
    return redirect("login")
