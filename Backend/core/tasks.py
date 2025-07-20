from celery import shared_task
from django.utils import timezone

from core.utils.analytics import AnalyticsManager
from core.utils.logger import logger
from metrics.models.platform import Platform


@shared_task
def update_analytics_cache():
    """
    Celery task to update all analytics caches.
    Should be scheduled to run periodically (e.g., every 30 minutes).
    """
    try:
        logger.info("Starting scheduled analytics cache update")
        results = AnalyticsManager.update_all_analytics()

        if 'error' in results:
            logger.error(f"Analytics cache update failed: {results['error']}")
            return False
        else:
            logger.info(f"Successfully updated all analytics caches: {results}")
            return True

    except Exception as e:
        logger.error(f"Failed to update analytics cache: {e}")
        return False


@shared_task
def refresh_platform_metrics():
    """
    Refresh metrics for all active platforms.
    Uses the cached platform list for efficiency.
    """
    start_time = timezone.now()
    logger.info("Starting scheduled platform metrics refresh")

    # Get platforms from cache for efficiency
    platforms = Platform.objects.get_all()

    success_count = 0
    failure_count = 0

    for platform in platforms:
        try:
            if platform.refresh_metrics():
                success_count += 1
            else:
                failure_count += 1
        except Exception as e:
            logger.error(f"Error refreshing metrics for {platform.name}: {e}")
            failure_count += 1

    duration = (timezone.now() - start_time).total_seconds()
    logger.info(
        f"Completed platform metrics refresh in {duration:.2f}s. "
        f"Success: {success_count}, Failures: {failure_count}"
    )

    # After refreshing metrics, update analytics as well
    update_analytics_cache.delay()

    return {
        "success_count": success_count,
        "failure_count": failure_count,
        "duration_seconds": duration
    }
