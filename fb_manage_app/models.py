from django.db import models
from django.contrib.auth.models import User

class FacebookPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page_id = models.CharField(max_length=255)
    page_name = models.CharField(max_length=255)
    access_token = models.TextField()
    permissions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.page_name