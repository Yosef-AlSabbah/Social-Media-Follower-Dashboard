from django.db import models


class FetchScript(models.Model):
    """
    Represents a script or scraper that fetches metrics from one or more social media platforms.
    Each script is uniquely identified and can be activated or deactivated.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Human‑friendly name for the fetch script (e.g. 'Facebook Scraper').",
    )
    script_path = models.CharField(
        max_length=255,
        help_text="Dotted path to your fetcher class, e.g. "
        "'fetchers.facebook.FacebookFetcher'",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this script was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this script was last updated.",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Fetch Script"
        verbose_name_plural = "Fetch Scripts"

    def __str__(self):
        return self.name
