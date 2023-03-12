from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Creates groups and permissions for the app'

    def handle(self, *args, **options):
        # create groups
        groups = [
            {'name': 'Super Admin', 'permissions': []},
            {'name': 'Admin', 'permissions': []},
            {'name': 'User', 'permissions': ['view_userprofile']},
        ]
        for group in groups:
            group_obj, created = Group.objects.get_or_create(name=group['name'])
            if created:
                self.stdout.write(self.style.SUCCESS(f"Group '{group_obj.name}' created successfully"))
            else:
                self.stdout.write(self.style.WARNING(f"Group '{group_obj.name}' already exists"))

            # assign permissions to group
            if group['permissions']:
                content_type = ContentType.objects.get_for_model(UserProfile)
                permissions = Permission.objects.filter(content_type=content_type, codename__in=group['permissions'])
                group_obj.permissions.set(permissions)
                self.stdout.write(self.style.SUCCESS(f"Permissions assigned to group '{group_obj.name}'"))
