from django.db import models
from user_authentication_models import User

class SystemParameter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_sensitive = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name

class NotificationTemplate(models.Model):
    CHANNEL_CHOICES = (
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('PUSH', 'Push Notification'),
        ('INAPP', 'In-App Notification'),
    )
    
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    body_template = models.TextField()
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
