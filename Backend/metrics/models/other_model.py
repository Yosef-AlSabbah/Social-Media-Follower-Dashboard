from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils import timezone

from core.utils.logger import logger
from metrics.models.platform import Platform


class DailyPlatformMetric(models.Model):
    """
    Stores daily metrics for a given platform, such as followers, engagement, and reach.
    Each record is unique per platform and date.
    """

    # ───────────────────────────────────── Fields ───────────────────────────���─────────
    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
        related_name="metrics",
        help_text="The platform this metric entry belongs to.",
    )
    date = models.DateField(
        help_text="Date for which the metrics are recorded.",
    )
    followers = models.PositiveIntegerField(
        help_text="Number of followers on this date.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this metric entry was created.",
    )

    # ───────────────────────────────── Dunder Methods ─────────────────────────────────
    def __str__(self):
        return f"{self.platform.name} - {self.date}"

    # ────────────────────────────────── Meta Options ──────────────────────────────────
    class Meta:
        db_table = "daily_platform_metrics"
        unique_together = ("platform", "date")
        indexes = [
            models.Index(fields=["date"]),
        ]
        ordering = ("-date",)
        verbose_name = "Daily Platform Metric"
        verbose_name_plural = "Daily Platform Metrics"

    # ───────────────────────────────── Class Methods ──────────────────────────────────
    @classmethod
    def create_daily_metric(cls, platform, date=None, followers=None):
        """
        Creates a daily platform metric entry for the given platform and date.
        Handles the unique constraint (platform, date) by using get_or_create.

        Args:
            platform (Platform): The platform instance to create metrics for
            date (date, optional): The date for the metric. Defaults to today.
            followers (int, optional): Number of followers. If None, fetches from platform.followers property.

        Returns:
            tuple: (DailyPlatformMetric instance, created boolean)

        Raises:
            ValidationError: If the platform is not active or other validation errors occur
        """
        if not platform.is_active:
            logger.warning(
                f"Attempted to create metric for inactive platform: {platform.name}"
            )
            raise ValidationError(
                f"Cannot create metrics for inactive platform: {platform.name}"
            )

        # Use today's date if not provided
        if date is None:
            date = timezone.now().date()

        # Get followers count if not provided
        if followers is None:
            followers = platform.followers

        # Validate followers count
        if followers is None or followers < 0:
            logger.error(
                f"Invalid followers count for platform {platform.name}: {followers}"
            )
            raise ValidationError(f"Invalid followers count: {followers}")

        try:
            # Use get_or_create to handle the unique constraint gracefully
            metric, created = cls.objects.get_or_create(
                platform=platform, date=date, defaults={"followers": followers}
            )

            if created:
                logger.info(
                    f"Created new daily metric for {platform.name} on {date}: {followers} followers"
                )
            else:
                logger.info(
                    f"Daily metric already exists for {platform.name} on {date}"
                )

            return metric, created

        except Exception as e:
            logger.error(
                f"Error creating daily metric for {platform.name} on {date}: {e}"
            )
            raise

    @classmethod
    def create_daily_metrics_for_all_platforms(cls, date=None):
        """
        Creates daily metrics for all active platforms for the given date.

        Args:
            date (date, optional): The date for the metrics. Defaults to today.

        Returns:
            dict: Summary of created metrics with platform names as keys and creation status as values
        """
        if date is None:
            date = timezone.now().date()

        results = {}
        active_platforms = Platform.objects.filter(is_active=True)

        logger.info(
            f"Creating daily metrics for {active_platforms.count()} active platforms on {date}"
        )

        for platform in active_platforms:
            try:
                metric, created = cls.create_daily_metric(platform, date)
                results[platform.name] = {
                    "created": created,
                    "followers": metric.followers,
                    "metric_id": metric.id,
                }
            except (ValidationError, Exception) as e:
                logger.error(f"Failed to create metric for {platform.name}: {e}")
                results[platform.name] = {"created": False, "error": str(e)}

        logger.info(f"Completed creating daily metrics. Results: {results}")
        return results

    @classmethod
    def get_analytics_summary(cls):
        """
        Retrieves analytics summary from the centralized AnalyticsManager.
        Does not compute new data - for updates use AnalyticsManager.update_analytics_summary()

        Returns:
            dict: Analytics summary with standardized structure
        """
        from core.utils.analytics import AnalyticsManager

        return AnalyticsManager.get_analytics_summary()

    @classmethod
    def calculate_period_growth(cls, start_date, end_date):
        """
        Calculates follower growth between two dates.
        Public method used by AnalyticsManager and other components.

        Args:
            start_date (date): Start date for growth calculation
            end_date (date): End date for growth calculation

        Returns:
            int: Net growth in followers during the period
        """
        try:
            start_metrics = (
                    cls.objects.filter(date=start_date).aggregate(total=Sum("followers"))[
                        "total"
                    ]
                    or 0
            )

            end_metrics = (
                    cls.objects.filter(date=end_date).aggregate(total=Sum("followers"))[
                        "total"
                    ]
                    or 0
            )

            growth = end_metrics - start_metrics
            logger.debug(f"Growth from {start_date} to {end_date}: {growth}")
            return growth

        except Exception as e:
            logger.error(
                f"Error calculating growth from {start_date} to {end_date}: {e}"
            )
            return 0
