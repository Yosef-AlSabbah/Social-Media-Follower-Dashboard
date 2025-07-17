from django.core.cache import cache
from django.utils import timezone
from .cache_keys import CacheKey


class PlatformCacheManager:
    """
    Centralized cache manager for platform metrics.
    Handles followers, delta, and last updated timestamps.
    """

    @staticmethod
    def get_platform_metrics(platform_name: str) -> dict:
        """
        Get all cached metrics for a platform.
        Returns dict with followers, delta, and last_updated.
        """
        followers_key = CacheKey.PLATFORM_FOLLOWERS.build(name=platform_name)
        delta_key = CacheKey.PLATFORM_DELTA.build(name=platform_name)
        last_updated_key = CacheKey.PLATFORM_LAST_UPDATED.build(name=platform_name)

        return {
            "followers": cache.get(followers_key),
            "delta": cache.get(delta_key),
            "last_updated": cache.get(last_updated_key),
        }

    @staticmethod
    def update_platform_metrics(platform_name: str, followers: int, delta: int = None):
        """
        Update all platform metrics in cache.
        Calculates delta if not provided by comparing with previous followers count.
        """
        followers_key = CacheKey.PLATFORM_FOLLOWERS.build(name=platform_name)
        delta_key = CacheKey.PLATFORM_DELTA.build(name=platform_name)
        last_updated_key = CacheKey.PLATFORM_LAST_UPDATED.build(name=platform_name)

        # Calculate delta if not provided
        if delta is None:
            previous_followers = cache.get(followers_key)
            delta = (
                (followers - previous_followers)
                if previous_followers is not None
                else 0
            )

        # Update all metrics
        cache.set(followers_key, followers, timeout=None)
        cache.set(delta_key, delta, timeout=None)
        cache.set(last_updated_key, timezone.now().isoformat(), timeout=None)

    @staticmethod
    def get_followers(platform_name: str) -> int:
        """Get cached followers count for a platform."""
        key = CacheKey.PLATFORM_FOLLOWERS.build(name=platform_name)
        return cache.get(key, 0)

    @staticmethod
    def get_delta(platform_name: str) -> int:
        """Get cached delta for a platform."""
        key = CacheKey.PLATFORM_DELTA.build(name=platform_name)
        return cache.get(key, 0)

    @staticmethod
    def get_last_updated(platform_name: str) -> str:
        """Get last updated timestamp for a platform."""
        key = CacheKey.PLATFORM_LAST_UPDATED.build(name=platform_name)
        return cache.get(key)

    @staticmethod
    def clear_platform_cache(platform_name: str):
        """Clear all cached data for a platform."""
        followers_key = CacheKey.PLATFORM_FOLLOWERS.build(name=platform_name)
        delta_key = CacheKey.PLATFORM_DELTA.build(name=platform_name)
        last_updated_key = CacheKey.PLATFORM_LAST_UPDATED.build(name=platform_name)

        cache.delete_many([followers_key, delta_key, last_updated_key])
