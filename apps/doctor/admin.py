from django.contrib import admin
from .models import Doctor, Speciality
from django.contrib import admin


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    ordering = ["user"]
    list_display = [
        "user",
        "title",
        "bio",
        "phone",
    ]
    list_filter = ["user"]

    fieldsets = (
        (None, {"fields": ["user", "title", "bio", "phone"]}),
        ("Specialities", {"fields": ["specialities"]}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "user",
                    "title",
                    "bio",
                    "phone",
                    "specialities",
                ],
            },
        ),
    )
    filter_horizontal = ("specialities",)


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = [
        "name",
        "description",
    ]
    list_filter = ["name"]

    fieldsets = ((None, {"fields": ["name", "description"]}),)

    add_fieldsets = (
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "name",
                    "description",
                ],
            },
        ),
    )
