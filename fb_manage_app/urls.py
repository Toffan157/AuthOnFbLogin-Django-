from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Web views
    path("", views.login_view, name="login"),
    path("facebook/callback/", views.facebook_callback, name="facebook_callback"),
    path("home/", views.home_view, name="home"),
    path("logout/", views.logout_view, name="logout"),

    # API auth
    path("api/login/", obtain_auth_token, name="api_login"),  # username/password login
    path("api/facebook/login/", views.api_facebook_login, name="api_facebook_login"),
    path("api/facebook/callback/", views.api_facebook_callback, name="api_facebook_callback"),

    # API endpoints for profile and pages
    path("api/profile/", views.api_user_profile, name="api_user_profile"),
    path("api/pages/", views.api_user_pages, name="api_user_pages"),
]