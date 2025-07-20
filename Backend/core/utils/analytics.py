"""
Core analytics utilities for generating dashboard statistics and summaries.
Contains reusable analytics functions and data structures.
"""

from datetime import date, timedelta

from django.core.cache import cache
from django.db.models import Sum
from django.utils import timezone

from core.utils.cache_keys import AnalyticsKeys
from core.utils.logger import logger
from metrics.models import DailyPlatformMetric, Platform
from metrics.serializers import AnalyticsSummarySerializer, DailyMetricSerializer


class AnalyticsManager:
    """
    A manager class for handling analytics data, including caching and calculations.
    Provides methods for retrieving summaries, trends, and daily metrics.
    """

    # ─────────────────────────────── Public Methods ───────────────────────────────

    @classmethod
    def get_analytics_summary(cls):
        """
        Retrieves the analytics summary from cache or computes it if not available.
        The summary includes total followers, top platform, and growth metrics.
        """
        summary = cache.get(AnalyticsKeys.ANALYTICS_SUMMARY)
        if summary is None:
            logger.info("Analytics summary cache miss. Calculating...")
            summary = cls._calculate_analytics_summary()
            cache.set(AnalyticsKeys.ANALYTICS_SUMMARY, summary, timeout=3600)  # Cache for 1 hour
        return summary

    @classmethod
    def get_growth_trends(cls):
        """
        Retrieves 7-day growth trends from cache or computes them if not available.
        """
        trends = cache.get(AnalyticsKeys.GROWTH_TRENDS)
        if trends is None:
            logger.info("Growth trends cache miss. Calculating...")
            trends = cls._calculate_growth_trends()
            cache.set(AnalyticsKeys.GROWTH_TRENDS, trends, timeout=3600)  # Cache for 1 hour
        return trends

    @classmethod
    def get_daily_metrics(cls) -> list:
        """Retrieves cached daily metrics"""
        cached_data = cache.get(AnalyticsKeys.DAILY_METRICS)
        if cached_data is None:
            logger.warning("Daily metrics cache miss - returning empty list")
            return []
        return cached_data

    @classmethod
    def invalidate_analytics_cache(cls):
        """
        Invalidates all analytics-related cache keys.
        """
        cache.delete(AnalyticsKeys.ANALYTICS_SUMMARY)
        cache.delete(AnalyticsKeys.GROWTH_TRENDS)
        cache.delete(AnalyticsKeys.DAILY_METRICS)
        logger.info("All analytics caches have been invalidated.")

    @classmethod
    def update_all_analytics(cls):
        """
        Calculates and caches all analytics data, including summary, trends, and daily metrics.
        """
        logger.info("Starting to update all analytics data...")

        # Calculate and cache the analytics summary
        summary = cls._calculate_analytics_summary()
        cache.set(AnalyticsKeys.ANALYTICS_SUMMARY, summary, timeout=3600)
        logger.info("Successfully updated and cached analytics summary.")

        # Calculate and cache growth trends
        trends = cls._calculate_growth_trends()
        cache.set(AnalyticsKeys.GROWTH_TRENDS, trends, timeout=3600)
        logger.info("Successfully updated and cached growth trends.")

        # Calculate and cache daily metrics
        daily_metrics = cls._calculate_daily_metrics()
        cache.set(AnalyticsKeys.DAILY_METRICS, daily_metrics, timeout=3600)
        logger.info("Successfully updated and cached daily metrics.")

        logger.info("All analytics data has been successfully updated and cached.")

    @staticmethod
    def _get_arabic_day_name(date_obj):
        """
        Returns the Arabic name of the day for a given date.
        """
        arabic_days = {
            "Monday": "الاثنين",
            "Tuesday": "الثلاثاء",
            "Wednesday": "الأربعاء",
            "Thursday": "الخميس",
            "Friday": "الجمعة",
            "Saturday": "السبت",
            "Sunday": "الأحد",
        }
        day_name_en = date_obj.strftime("%A")
        return arabic_days.get(day_name_en, "")

    @classmethod
    def _calculate_analytics_summary(cls):
        """
        Calculates the analytics summary by querying the database.
        - Total followers across all platforms.
        - Top platform by follower count.
        - Daily, weekly, and monthly growth.
        """
        today = date.today()
        yesterday = today - timedelta(days=1)
        seven_days_ago = today - timedelta(days=7)
        thirty_days_ago = today - timedelta(days=30)

        active_platforms = Platform.objects.filter(is_active=True)
        if not active_platforms:
            return {
                "total_followers": 0,
                "top_platform": None,
                "daily_growth": 0,
                "weekly_growth": 0,
                "monthly_growth": 0,
            }

        total_followers = sum(p.followers for p in active_platforms)

        # Find the top platform based on today's metrics
        top_platform = None
        if total_followers > 0:
            top_platform_instance = max(active_platforms, key=lambda p: p.followers)
            top_platform = {
                "id": top_platform_instance.id,
                "name": top_platform_instance.name,
                "name_ar": top_platform_instance.name_ar,
                "followers": top_platform_instance.followers,
            }

        # Calculate growth metrics
        daily_growth = cls._calculate_growth(today, yesterday)
        weekly_growth = cls._calculate_growth(today, seven_days_ago)
        monthly_growth = cls._calculate_growth(today, thirty_days_ago)

        return {
            "total_followers": total_followers,
            "top_platform": top_platform,
            "daily_growth": daily_growth,
            "weekly_growth": weekly_growth,
            "monthly_growth": monthly_growth,
        }

    @classmethod
    def _calculate_growth(cls, current_date, past_date):
        """
        Helper method to calculate follower growth between two dates.
        """
        # Check if there is data for the past date
        if not DailyPlatformMetric.objects.filter(date=past_date).exists():
            return 0

        current_followers = (
                DailyPlatformMetric.objects.filter(date=current_date).aggregate(
                    Sum("followers")
                )["followers__sum"]
                or 0
        )
        past_followers = (
                DailyPlatformMetric.objects.filter(date=past_date).aggregate(
                    Sum("followers")
                )["followers__sum"]
                or 0
        )

        return current_followers - past_followers

    @classmethod
    def _calculate_growth_trends(cls):
        """
        Calculates the 7-day follower growth trends for each platform.
        """
        today = date.today()
        start_date = today - timedelta(days=6)

        # Get all active platforms
        platforms = Platform.objects.filter(is_active=True)

        # Fetch all relevant metrics in a single query
        metrics = DailyPlatformMetric.objects.filter(
            platform__in=platforms,
            date__gte=start_date,
            date__lte=today
        ).values('platform_id', 'date', 'followers')

        # Organize metrics by platform and date for easy lookup
        metrics_by_platform = {}
        for metric in metrics:
            pid = metric['platform_id']
            if pid not in metrics_by_platform:
                metrics_by_platform[pid] = {}
            metrics_by_platform[pid][metric['date']] = metric['followers']

        # Build the trend data
        trends = []
        for platform in platforms:
            platform_data = []
            # Only include data for days where metrics exist
            for day_offset in range(7):
                current_date = start_date + timedelta(days=day_offset)
                if platform.id in metrics_by_platform and current_date in metrics_by_platform[platform.id]:
                    followers = metrics_by_platform[platform.id][current_date]
                    platform_data.append({
                        "day": cls._get_arabic_day_name(current_date),
                        "value": followers,
                        "date": current_date.isoformat(),
                    })

            if platform_data:
                trends.append({
                    "platform_id": platform.id,
                    "data": platform_data,
                })

        return trends

    @classmethod
    def _calculate_daily_metrics(cls) -> list:
        """Computes daily metrics for the last 30 days"""
        today = timezone.now().date()
        daily_data = []

        for i in range(30):  # Last 30 days
            target_date = today - timedelta(days=29 - i)  # Start from 29 days ago
            previous_date = target_date - timedelta(days=1)

            # Get total followers for target date
            current_total = (
                    DailyPlatformMetric.objects.filter(date=target_date).aggregate(
                        total=Sum("followers")
                    )["total"]
                    or 0
            )

            # Get total followers for previous date
            previous_total = (
                    DailyPlatformMetric.objects.filter(date=previous_date).aggregate(
                        total=Sum("followers")
                    )["total"]
                    or 0
            )

            # Calculate new followers (growth)
            new_followers = max(0, current_total - previous_total)

            daily_data.append(
                {"date": target_date.isoformat(), "new_followers": new_followers}
            )

        # Validate data
        serializer = DailyMetricSerializer(data=daily_data, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @staticmethod
    def _get_default_summary() -> dict:
        """Returns a safe default summary for error cases"""
        default_data = {
            "total_followers": 0,
            "top_platform": {
                "id": "0",  # Use "0" instead of empty string to pass validation
                "name": "No Data",
                "name_ar": "لا توجد بيانات",
                "followers": 0,
            },
            "daily_growth": 0,
            "weekly_growth": 0,
            "monthly_growth": 0,
        }

        # Validate default data through serializer
        serializer = AnalyticsSummarySerializer(data=default_data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data
