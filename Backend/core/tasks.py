from celery import shared_task
from django.utils import timezone

from core.utils.analytics import AnalyticsManager
from core.utils.logger import logger


@shared_task
def update_analytics_cache():
    """
    Celery task to update all analytics caches.
    Should be scheduled to run periodically (e.g., every 30 minutes).
    """
    try:
        logger.info("Starting scheduled analytics cache update")
        results = AnalyticsManager.update_all_analytics()

        if "error" in results:
            logger.error(f"Analytics cache update failed: {results['error']}")
            return False
        else:
            logger.info(f"Successfully updated all analytics caches: {results}")
            return True

    except Exception as e:
        logger.error(f"Failed to update analytics cache: {e}")
        return False
