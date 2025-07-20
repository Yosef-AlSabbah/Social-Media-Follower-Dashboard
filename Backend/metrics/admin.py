from django.contrib import admin
from django import forms
from django.utils.html import format_html

from .models import DailyPlatformMetric, FetchScript, Platform
from .widgets import ColorPickerWidget


class PlatformAdminForm(forms.ModelForm):
    """Custom form for Platform admin with color picker widget"""

    class Meta:
        model = Platform
        fields = "__all__"
        widgets = {
            "color": ColorPickerWidget(),
        }


@admin.register(FetchScript)
class FetchScriptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "script_path",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "script_path")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "script_path",
                )
            },
        ),
        (
            "System Info",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Platform model.
    """

    form = PlatformAdminForm
    list_display = (
        "id",
        "name",
        "name_ar",
        "page_url",
        "fetch_script",
        "followers",
        "delta",
        "display_color",  # Use the custom method here
        "is_active",
        "last_updated",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = ("name", "name_ar")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at", "last_updated")
    fieldsets = (
        (
            "Platform Information",
            {
                "fields": (
                    "id",
                    "name",
                    "name_ar",
                    "page_url",
                    "fetch_script",
                    "color",
                    "is_active",
                )
            },
        ),
        ("Timestamps", {"fields": ("last_updated", "created_at", "updated_at")}),
    )

    def display_color(self, obj):
        """
        Create a colored circle for the list display.
        """
        if obj.color:
            return format_html(
                '<div style="width: 25px; height: 25px; background-color: {0}; border-radius: 50%;"></div>',
                obj.color,
            )
        return "No color"

    display_color.short_description = "Color"


@admin.register(DailyPlatformMetric)
class DailyPlatformMetricAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "platform",
        "date",
        "followers",
        "created_at",
    )
    search_fields = ("platform__name",)
    list_filter = ("date", "platform__name")
    readonly_fields = ("created_at",)
    ordering = ("-date", "-followers")
    fieldsets = (
        (
            "Metric Information",
            {
                "fields": (
                    "id",
                    "platform",
                    "date",
                    "followers",
                )
            },
        ),
        ("Timestamps", {"fields": ("created_at",)}),
    )
