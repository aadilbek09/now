from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create a default superuser if it does not exist"

    def handle(self, *args, **options):
        User = get_user_model()
        username = "admin123"
        password = "1234"
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": "admin@example.com", "is_superuser": True, "is_staff": True},
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.email = "admin@example.com"
        user.save()
        if created:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' password reset to '{password}'"))
