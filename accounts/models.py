from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "USER", "User"
        FACILITY_MANAGER = "FACILITY_MANAGER", "Facility Manager"
        SYSTEM_ADMIN = "SYSTEM_ADMIN", "System Admin"

    role = models.CharField(max_length=30, choices=Role.choices, default=Role.USER)
    account_status = models.CharField(max_length=30, default="active")

    def is_facility_manager(self):
        return self.role == self.Role.FACILITY_MANAGER

    def is_system_admin(self):
        return self.role == self.Role.SYSTEM_ADMIN


class Team(models.Model):
    name = models.CharField(max_length=150)
    representative = models.ForeignKey(
        User,
        related_name="teams",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
