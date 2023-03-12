from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):

    
    role_choices = [
        ('SA', 'Super Admin'),
        ('A', 'Admin'),
        ('U', 'User')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='accounts_profile', default=User.objects.first().id)

    role = models.CharField(max_length=2, choices=role_choices, default='U')
