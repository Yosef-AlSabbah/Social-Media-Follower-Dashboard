from enum import Enum


class CacheKey(Enum):
    """
    Centralized cache key definitions for the whole app.
    Use build() method to generate dynamic keys.
    """

    PLATFORM_FOLLOWERS = "platform_followers_{name}"
    PLATFORM_DELTA = "platform_delta_{name}"
    PLATFORM_LAST_UPDATED = "platform_last_updated_{name}"

    def build(self, **kwargs) -> str:
        """
        Returns the formatted cache key for this enum value.
        """
        return self.value.format(**kwargs)


class AnalyticsKeys:
    """
    Cache keys for analytics data.
    Centralizes all analytics-related cache keys for easier management.
    """

    PREFIX = "analytics"
    ANALYTICS_SUMMARY = f"{PREFIX}:summary"
    TOP_PLATFORM = f"{PREFIX}:top_platform"
    TOTAL_FOLLOWERS = f"{PREFIX}:total_followers"
    GROWTH_TRENDS = f"{PREFIX}:growth_trends"
    DAILY_METRICS = f"{PREFIX}:daily_metrics"

    @classmethod
    def get_platform_growth_key(cls, platform_name: str, period: str) -> str:
        """Generate cache key for platform growth metrics"""
        return f"{cls.PREFIX}:growth:{platform_name}:{period}"
