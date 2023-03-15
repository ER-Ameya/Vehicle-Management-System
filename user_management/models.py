from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile",default=User.objects.first().id)

    role_choices = [
        ('SA', 'Super Admin'),
        ('A', 'Admin'),
        ('U', 'User')
    ]
    role = models.CharField(max_length=2, choices=role_choices)

    def __str__(self):
        print(self.user.usename)
        return self.user.username
