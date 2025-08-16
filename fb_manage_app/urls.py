from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("facebook/callback/", views.facebook_callback, name="facebook_callback"),
    path("home/", views.home_view, name="home"),
    path("logout/", views.logout_view, name="logout"),
]