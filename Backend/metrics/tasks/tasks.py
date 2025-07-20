"""
Metrics-specific Celery tasks.
This module contains tasks for platform metrics, analytics, and reporting.
"""
from celery import shared_task

from core.utils.analytics import AnalyticsManager
from core.utils.logger import logger
from metrics.models.platform import Platform
from metrics.tasks.registry import register_task


# Task implementations that will be registered with both TaskRegistry and Celery
@register_task
def update_platform_metrics():
    """
    Updates metrics for all active platforms.
    Automatically registered with TaskRegistry and Celery.
    """
    platforms = Platform.objects.get_all()
    results = {}

    for platform in platforms:
        try:
            success = platform.refresh_metrics()
            results[platform.name] = success
        except Exception as e:
            logger.error(f"Error refreshing metrics for {platform.name}: {e}")
            results[platform.name] = False

    return results


@register_task
def update_analytics_cache():
    """
    Updates analytics cache with fresh data.
    Automatically registered with TaskRegistry and Celery.
    """
    try:
        AnalyticsManager.update_all_analytics()
        logger.info("Successfully updated all analytics caches.")
        return {"success": True}
    except Exception as e:
        logger.error(f"Error updating analytics cache: {e}")
        return {"success": False, "error": str(e)}


@register_task
def create_daily_platform_metrics():
    """
    Creates daily metrics records for all active platforms.
    Automatically registered with TaskRegistry and Celery.
    """
    from metrics.models.other_model import DailyPlatformMetric
    return DailyPlatformMetric.create_daily_metrics_for_all_platforms()


# Shared task for Celery Beat scheduling - executes all registered tasks
@shared_task
def execute_all_metrics_tasks():
    """
    Executes all tasks registered in the TaskRegistry.
    This is the main entry point for scheduled task execution.
    """
    from metrics.tasks.registry import TaskRegistry

    logger.info("Starting execution of all metrics tasks")
    results = TaskRegistry.execute_all_tasks()

    # Count successes and failures
    successes = sum(1 for r in results.values() if r.get('success', False))
    failures = len(results) - successes

    logger.info(f"Task execution completed: {successes} succeeded, {failures} failed")
    return results
