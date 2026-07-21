from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Foydalanuvchi (User) va Admin uchun umumiy jadval.
    role maydoni orqali oddiy mijoz (user) va admin ajratiladi.
    """

    class Role(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        help_text="Foydalanuvchi turi: user yoki admin",
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    bio = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN
