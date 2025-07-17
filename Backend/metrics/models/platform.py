import uuid

from django.db import models

from core.utils.logger import logger
from core.utils.platform_cache import PlatformCacheManager
from fetchers import run_fetcher
from metrics.models.fetch_script import FetchScript


class PlatformManager(models.Manager):
    """
    Custom manager for Platform model to filter only active platforms by default.
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Platform(models.Model):
    """
    Represents a social media platform (e.g. Facebook, Twitter) that is tracked for metrics.
    Each platform can be associated with a fetch script and has a unique UUID.
    """

    # ───────────────────────────────────── Fields ─────────────────────────────────────
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        help_text="Unique identifier for the platform. Auto-generated.",
    )
    name = models.CharField(
        max_length=100,
        help_text="Platform name in English (e.g. 'Facebook').",
    )
    name_ar = models.CharField(
        max_length=100,
        help_text="Platform name in Arabic.",
    )
    page_url = models.URLField(
        "Page URL",
        max_length=300,
        blank=True,
        help_text="URL to the platform page (e.g. https://facebook.com/YourPage).",
    )
    # The fetch_script field links to the script responsible for fetching this platform's metrics.
    fetch_script = models.OneToOneField(
        FetchScript,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="platform",
        help_text="Script to run for pulling this platform’s metrics.",
    )
    color = models.CharField(
        max_length=7,
        help_text="Hex color code for the platform (e.g. '#4267B2').",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates if this platform is currently active and tracked.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when this platform was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when this platform was last updated."
    )

    objects = PlatformManager()

    # ───────────────────────────────── Dunder Methods ─────────────────────────────────
    def __str__(self):
        return self.name

    # ────────────────────────────────── Meta Options ──────────────────────────────────
    class Meta:
        db_table = "platforms"
        verbose_name = "Platform"
        verbose_name_plural = "Platforms"
        indexes = [
            models.Index(fields=["name"]),
        ]
        ordering = ("name",)

    # ────────────────────────────────── Properties ──────────────────────────────────
    @property
    def followers(self):
        """
        Returns the number of followers for the platform on the current date.
        Uses the centralized cache manager for maintainability.
        """
        return PlatformCacheManager.get_followers(self.name)

    @property
    def delta(self):
        """
        Returns the change in followers since the last update.
        Uses centralized cache manager.
        """
        return PlatformCacheManager.get_delta(self.name)

    @property
    def last_updated(self):
        """
        Returns the timestamp when the metrics were last updated.
        Uses centralized cache manager.
        """
        return PlatformCacheManager.get_last_updated(self.name)

    def refresh_metrics(self):
        """
        Force refresh of platform metrics and update cache.
        Useful for scheduled tasks or manual updates.
        """
        try:
            new_followers = run_fetcher(self)
            PlatformCacheManager.update_platform_metrics(self.name, new_followers)
            logger.info(
                f"Successfully refreshed metrics for {self.name}: {new_followers} followers"
            )
            return True
        except (KeyError, ValueError, TypeError, AttributeError) as e:
            logger.error(f"Error refreshing metrics for {self.name}: {e}")
            return False
