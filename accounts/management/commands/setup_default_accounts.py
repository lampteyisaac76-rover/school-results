import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Ensure default administrator and teacher accounts exist in production"

    def handle(self, *args, **options):
        # 1. Superuser / Administrator
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@school.com')

        admin_user, admin_created = User.objects.get_or_create(
            username=admin_username,
            defaults={
                'is_staff': True,
                'is_superuser': True,
                'email': admin_email,
            }
        )
        admin_user.set_password(admin_password)
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

        action = "Created" if admin_created else "Updated"
        self.stdout.write(self.style.SUCCESS(
            f"{action} administrator account: username='{admin_username}'"
        ))

        # 2. Shared Teacher Account (non-staff)
        teacher_username = os.environ.get('TEACHER_USERNAME', 'teacher')
        teacher_password = os.environ.get('TEACHER_PASSWORD', 'teacher123')

        teacher_user, teacher_created = User.objects.get_or_create(
            username=teacher_username,
            defaults={
                'is_staff': False,
                'is_superuser': False,
            }
        )
        teacher_user.set_password(teacher_password)
        teacher_user.is_staff = False
        teacher_user.is_superuser = False
        teacher_user.save()

        t_action = "Created" if teacher_created else "Updated"
        self.stdout.write(self.style.SUCCESS(
            f"{t_action} teacher account: username='{teacher_username}'"
        ))
