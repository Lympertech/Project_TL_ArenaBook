from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Team, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "role", "account_status", "is_staff")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("ArenaBook", {"fields": ("role", "account_status")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("ArenaBook", {"fields": ("role", "account_status")}),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "representative")
