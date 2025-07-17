"""
Core analytics utilities for generating dashboard statistics and summaries.
Contains reusable analytics functions and data structures.
"""

from datetime import timedelta, date
from django.utils import timezone
from django.db.models import Sum, Max
from django.core.cache import cache

from core.utils.logger import logger
from core.utils.cache_keys import AnalyticsKeys
from metrics.models.platform import Platform
from metrics.serializers import (
    AnalyticsSummarySerializer,
    GrowthTrendSerializer,
    DailyMetricSerializer,
)


class AnalyticsManager:
    """
    Centralized manager for analytics operations.
    Handles computation and caching of analytics data.
    """

    # === Arabic day names mapping ===
    ARABIC_DAYS = {
        0: "الاثنين",  # Monday
        1: "الثلاثاء",  # Tuesday
        2: "الأربعاء",  # Wednesday
        3: "الخميس",  # Thursday
        4: "الجمعة",  # Friday
        5: "السبت",  # Saturday
        6: "الأحد",  # Sunday
    }

    @classmethod
    def update_all_analytics(cls) -> dict:
        """
        Updates all analytics data and caches. Called by Celery task.

        Returns:
            dict: Summary of update results
        """
        results = {}

        try:
            # Update analytics summary
            summary = cls._compute_analytics_summary()
            cache.set(AnalyticsKeys.ANALYTICS_SUMMARY, summary)
            results["summary"] = "success"
            logger.info("Updated analytics summary cache")

            # Update growth trends
            trends = cls._compute_growth_trends()
            cache.set(AnalyticsKeys.GROWTH_TRENDS, trends)
            results["growth_trends"] = "success"
            logger.info("Updated growth trends cache")

            # Update daily metrics
            daily_metrics = cls._compute_daily_metrics()
            cache.set(AnalyticsKeys.DAILY_METRICS, daily_metrics)
            results["daily_metrics"] = "success"
            logger.info("Updated daily metrics cache")

            logger.info("Successfully updated all analytics caches")

        except Exception as e:
            logger.error(f"Error updating analytics: {e}")
            results["error"] = str(e)

        return results

    @classmethod
    def get_analytics_summary(cls) -> dict:
        """Retrieves cached analytics summary"""
        cached_data = cache.get(AnalyticsKeys.ANALYTICS_SUMMARY)
        if cached_data is None:
            logger.warning("Analytics summary cache miss - returning defaults")
            return cls._get_default_summary()
        return cached_data

    @classmethod
    def get_growth_trends(cls) -> list:
        """Retrieves cached growth trends"""
        cached_data = cache.get(AnalyticsKeys.GROWTH_TRENDS)
        if cached_data is None:
            logger.warning("Growth trends cache miss - returning empty list")
            return []
        return cached_data

    @classmethod
    def get_daily_metrics(cls) -> list:
        """Retrieves cached daily metrics"""
        cached_data = cache.get(AnalyticsKeys.DAILY_METRICS)
        if cached_data is None:
            logger.warning("Daily metrics cache miss - returning empty list")
            return []
        return cached_data

    @classmethod
    def _compute_analytics_summary(cls) -> dict:
        """Computes fresh analytics summary"""
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        # Get active platforms and their current metrics
        active_platforms = Platform.objects.filter(is_active=True)

        # Calculate total followers
        total_followers = sum(platform.followers or 0 for platform in active_platforms)

        # Find top platform
        top_platform = None
        max_followers = 0

        for platform in active_platforms:
            current_followers = platform.followers or 0
            if current_followers > max_followers:
                max_followers = current_followers
                top_platform = platform

        # Prepare top platform data
        top_platform_data = {
            "id": str(top_platform.id) if top_platform else "",
            "name": top_platform.name if top_platform else "No platforms",
            "name_ar": top_platform.name_ar if top_platform else "لا توجد منصات",
            "followers": max_followers,
        }

        # Calculate growth metrics
        from metrics.models.other_model import DailyPlatformMetric

        daily_growth = DailyPlatformMetric.calculate_period_growth(yesterday, today)
        weekly_growth = DailyPlatformMetric.calculate_period_growth(week_ago, today)
        monthly_growth = DailyPlatformMetric.calculate_period_growth(month_ago, today)

        # Construct and validate analytics summary
        summary_data = {
            "total_followers": total_followers,
            "top_platform": top_platform_data,
            "daily_growth": daily_growth,
            "weekly_growth": weekly_growth,
            "monthly_growth": monthly_growth,
        }

        serializer = AnalyticsSummarySerializer(data=summary_data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @classmethod
    def _compute_growth_trends(cls) -> list:
        """Computes growth trends for the last 7 days for all platforms"""
        from metrics.models.other_model import DailyPlatformMetric

        today = timezone.now().date()
        trends_data = []

        active_platforms = Platform.objects.all()

        for platform in active_platforms:
            platform_data = {
                "platform_id": platform,  # Pass the Platform instance, not string ID
                "data": [],
            }

            # Get last 7 days of data
            for i in range(7):
                target_date = today - timedelta(
                    days=6 - i
                )  # Start from 6 days ago to today

                # Get metric for this date
                try:
                    metric = DailyPlatformMetric.objects.get(
                        platform=platform, date=target_date
                    )
                    followers_count = metric.followers
                except DailyPlatformMetric.DoesNotExist:
                    followers_count = platform.followers or 0

                # Get Arabic day name
                day_name = cls.ARABIC_DAYS.get(target_date.weekday(), "غير معروف")

                data_point = {
                    "day": day_name,
                    "value": followers_count,
                    "date": target_date.isoformat(),
                }
                platform_data["data"].append(data_point)

            trends_data.append(platform_data)

        # Validate data
        serializer = GrowthTrendSerializer(data=trends_data, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @classmethod
    def _compute_daily_metrics(cls) -> list:
        """Computes daily metrics for the last 30 days"""
        from metrics.models.other_model import DailyPlatformMetric

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
                "id": "",
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
