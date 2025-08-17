from rest_framework import serializers
from .models import FacebookPage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name']

class FacebookPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookPage
        fields = ['page_id', 'page_name', 'access_token', 'permissions']