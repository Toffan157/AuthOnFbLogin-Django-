from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import requests

from .models import FacebookPage


# -------------------------------------------------------------------
# Helper to fetch and save pages
# -------------------------------------------------------------------
def fetch_and_store_pages(user, access_token):
    """Fetch all pages managed by user and store in DB"""
    accounts_url = f"https://graph.facebook.com/v23.0/me/accounts"
    accounts_resp = requests.get(accounts_url, params={
        "access_token": access_token,
        "fields": "id,name,access_token,perms"
    }).json()

    pages = accounts_resp.get("data", [])
    for page in pages:
        FacebookPage.objects.update_or_create(
            user=user,
            page_id=page["id"],
            defaults={
                "page_name": page["name"],
                "access_token": page["access_token"],
                "permissions": page.get("perms", []),
            }
        )
    return pages


# -------------------------------------------------------------------
# Web views
# -------------------------------------------------------------------
def login_view(request):
    fb_login_url = (
        f"https://www.facebook.com/v23.0/dialog/oauth?"
        f"client_id={settings.FACEBOOK_CLIENT_ID}"
        f"&redirect_uri={settings.FACEBOOK_REDIRECT_URI}"
        f"&scope=email,pages_show_list,pages_read_engagement"
    )
    return render(request, "login.html", {"fb_login_url": fb_login_url})


def facebook_callback(request):
    code = request.GET.get("code")
    if not code:
        return redirect("login")

    # 1. Exchange code for access token
    token_url = (
        f"https://graph.facebook.com/v23.0/oauth/access_token?"
        f"client_id={settings.FACEBOOK_CLIENT_ID}"
        f"&redirect_uri={settings.FACEBOOK_REDIRECT_URI}"
        f"&client_secret={settings.FACEBOOK_CLIENT_SECRET}"
        f"&code={code}"
    )
    token_response = requests.get(token_url).json()
    access_token = token_response.get('access_token')

    if not access_token:
        return redirect("login")

    # 2. Get user info
    user_info = requests.get(
        f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"
    ).json()

    email = user_info.get("email", f"{user_info['id']}@facebook.com")
    name = user_info.get("name", "Facebook User")

    # 3. Create or get Django user
    user, created = User.objects.get_or_create(
        username=email,
        defaults={'first_name': name}
    )

    # 4. Create/get DRF token
    token, _ = Token.objects.get_or_create(user=user)

    # 5. Login user
    login(request, user)

    # 6. Fetch and save pages in DB
    fetch_and_store_pages(user, access_token)

    # 7. Redirect to home with token
    return render(request, "home.html", {
        "user": user,
        "auth_token": token.key
    })


def home_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "home.html", {"user": request.user})


def logout_view(request):
    logout(request)
    return redirect("login")


# -------------------------------------------------------------------
# API views
# -------------------------------------------------------------------
@api_view(["GET"])
def api_facebook_login(request):
    """API endpoint to redirect user to FB login"""
    fb_login_url = (
        f"https://www.facebook.com/v23.0/dialog/oauth?"
        f"client_id={settings.FACEBOOK_CLIENT_ID}"
        f"&redirect_uri={settings.FACEBOOK_REDIRECT_URI}"
        f"&scope=email,pages_show_list,pages_read_engagement"
    )
    return Response({"login_url": fb_login_url})


@api_view(["GET"])
@permission_classes([AllowAny])        
@authentication_classes([])
def api_facebook_callback(request):
    """API callback after FB login"""
    code = request.GET.get("code")
    if not code:
        return Response({"error": "Authorization code not provided"}, status=400)

    # Exchange code for token
    token_url = (
        f"https://graph.facebook.com/v23.0/oauth/access_token?"
        f"client_id={settings.FACEBOOK_CLIENT_ID}"
        f"&redirect_uri={settings.FACEBOOK_REDIRECT_URI}"
        f"&client_secret={settings.FACEBOOK_CLIENT_SECRET}"
        f"&code={code}"
    )
    token_response = requests.get(token_url).json()
    access_token = token_response.get("access_token")

    if not access_token:
        return Response({"error": "Failed to obtain access token"}, status=400)

    # Get user info
    user_info = requests.get(
        f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"
    ).json()

    email = user_info.get("email", f"{user_info['id']}@facebook.com")
    name = user_info.get("name", "Facebook User")

    # Create/get user
    user, _ = User.objects.get_or_create(username=email, defaults={"first_name": name})

    # Fetch and save pages
    pages = fetch_and_store_pages(user, access_token)

    # Create/get token
    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "token": token.key,
        "user": {
            "id": user.id,
            "email": user.username,
            "name": name,
            "facebook_id": user_info.get("id"),
        },
        "pages": pages
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_user_pages(request):
    """List stored pages for logged-in user"""
    pages = FacebookPage.objects.filter(user=request.user)
    data = [
        {
            "page_id": p.page_id,
            "page_name": p.page_name,
            "permissions": p.permissions,
            "access_token": p.access_token
        }
        for p in pages
    ]
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_user_profile(request):
    """Return user profile info"""
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "first_name": request.user.first_name,
    })