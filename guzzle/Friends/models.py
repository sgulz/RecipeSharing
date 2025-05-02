from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
    statusChoices = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_sent')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_received')
    status = models.CharField(max_length=10, choices=statusChoices, default='pending')
    