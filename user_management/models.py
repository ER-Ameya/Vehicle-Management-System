from django.db import models
from django.contrib.auth.models import User, Group

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
    
    # def save(self, *args, **kwargs):
    #     """
    #     Override the save method to add new users to the "user" group by default.
    #     """
    #     is_new_user = self.pk is None  # Check if the object is a new user being created
    #     super().save(*args, **kwargs)
    #     if is_new_user:
    #         group = Group.objects.get(name='user')
    #         self.user.groups.add(group)
    #         self.user.save()
