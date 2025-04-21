from django.contrib import admin
from apps.account.models import UserAccount
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


@admin.register(UserAccount)
class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]
    list_filter = ["is_active", "is_staff", "is_superuser", "created_at"]

    fieldsets = (
        (None, {"fields": ["email", "username", "password"]}),
        ("Personal Info", {"fields": ["first_name", "last_name"]}),
        (
            "Permissions",
            {
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ]
            },
        ),
        (
            "Important dates",
            {"fields": ["last_login", "created_at", "updated_at"]},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ],
            },
        ),
    )

    search_fields = ["email", "username", "first_name", "last_name"]

    readonly_fields = ["created_at", "updated_at"]
