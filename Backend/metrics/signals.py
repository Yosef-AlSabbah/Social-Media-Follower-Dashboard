from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib import messages
from django.core.cache import cache

from core.utils.logger import logger
from metrics.models import Platform


def trigger_platform_tasks(platform_name, action):
    """
    Centralized function to trigger all metrics tasks and invalidate cache
    when Platform operations occur.

    Args:
        platform_name (str): Name of the platform that was modified
        action (str): Action performed ('created', 'updated', 'deleted')
    """
    # Create a unique cache key to prevent duplicate executions
    cache_key = f"platform_signal_debounce:{platform_name}:{action}:{timezone.now().strftime('%Y%m%d%H%M%S')}"

    # Check if this exact operation was already triggered recently (within 5 seconds)
    if cache.get(cache_key):
        logger.info(f"Skipping duplicate signal for Platform '{platform_name}' {action}")
        return None

    # Set the cache key to prevent duplicates for 5 seconds
    cache.set(cache_key, True, 5)

    logger.info(f"Platform '{platform_name}' was {action}. Triggering system tasks...")

    # Invalidate platform cache since data changed
    try:
        from metrics.models.platform import PlatformManager
        manager = PlatformManager()
        manager.invalidate_cache()
        logger.info(f"Platform cache invalidated due to Platform {action}")
    except Exception as e:
        logger.error(f"Failed to invalidate platform cache: {e}")

    # Import here to avoid circular imports
    try:
        from metrics.tasks.tasks import execute_all_metrics_tasks

        # Trigger all metrics tasks asynchronously with a small delay
        task = execute_all_metrics_tasks.apply_async(countdown=3)

        logger.info(
            f"All metrics tasks triggered due to Platform {action} "
            f"(Platform: {platform_name}, Task ID: {task.id})"
        )

        return task.id

    except ImportError as e:
        logger.error(f"Could not import metrics tasks: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to trigger metrics tasks after Platform {action}: {e}")
        return None


@receiver(post_save, sender=Platform)
def platform_saved_handler(sender, instance, created, **kwargs):
    """
    Signal handler that triggers all metrics tasks when a Platform is created or updated.

    Args:
        sender: The model class (Platform)
        instance: The actual Platform instance that was saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    action = "created" if created else "updated"
    trigger_platform_tasks(instance.name, action)


@receiver(post_delete, sender=Platform)
def platform_deleted_handler(sender, instance, **kwargs):
    """
    Signal handler that triggers all metrics tasks when a Platform is deleted.

    Args:
        sender: The model class (Platform)
        instance: The Platform instance that was deleted
        **kwargs: Additional keyword arguments
    """
    trigger_platform_tasks(instance.name, "deleted")
