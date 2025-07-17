from django.contrib import admin

from .models import Platform


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "name_ar",
        "followers",
        "delta",
        "color",
        "is_active",
        "last_updated",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active", "color")
    search_fields = ("name", "name_ar", "page_url")
    readonly_fields = ("followers", "delta", "last_updated", "created_at", "updated_at")
    ordering = ("name",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "name",
                    "name_ar",
                    "page_url",
                    "fetch_script",
                    "color",
                    "is_active",
                    "followers",
                    "delta",
                    "last_updated",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
