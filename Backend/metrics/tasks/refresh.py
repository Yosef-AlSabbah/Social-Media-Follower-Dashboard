from celery import shared_task
from core.utils.logger import logger
from metrics.models import Platform


@shared_task(name="force_refresh_platforms")
def force_refresh_platforms():
    """
    A Celery task to force-refresh metrics for all active platforms.
    This task is triggered on-demand via an API endpoint.
    """
    logger.info("Starting on-demand platform metric refresh...")
    platforms = Platform.objects.filter(is_active=True)
    refreshed_count = 0
    for platform in platforms:
        try:
            if platform.refresh_metrics():
                refreshed_count += 1
        except Exception as e:
            logger.error(f"Error during force-refresh for {platform.name}: {e}")

    logger.info(f"Force-refresh completed. {refreshed_count}/{len(platforms)} platforms refreshed.")

