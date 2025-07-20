from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.management import call_command

from core.utils.logger import logger


class Command(BaseCommand):
    """
    Management command to trigger Celery tasks immediately on system startup.

    This command can be run during startup to ensure all metrics and analytics
    are refreshed without waiting for the scheduled Celery Beat tasks.

    Usage: python manage.py trigger_startup_tasks
    """

    help = "Triggers all registered metrics tasks immediately"

    def handle(self, *args, **options):
        start_time = timezone.now()
        self.stdout.write(self.style.SUCCESS("Starting initial system tasks..."))
        logger.info("Triggering startup tasks via management command")

        # First, ensure all FetchScript entries are populated
        self.stdout.write("Ensuring FetchScript entries are populated...")
        try:
            call_command('populate_fetch_scripts')
            self.stdout.write(self.style.SUCCESS("✓ FetchScript population completed"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ FetchScript population failed: {e}"))
            logger.error(f"FetchScript population failed: {e}")

        # Import here to ensure all task registration has happened
        from metrics.tasks.tasks import execute_all_metrics_tasks

        # Execute all registered tasks immediately
        self.stdout.write("Executing all registered metrics tasks...")
        task = execute_all_metrics_tasks.apply_async(countdown=1)
        self.stdout.write(self.style.SUCCESS(f"Tasks scheduled (task ID: {task.id})"))

        # Display task count (for informational purposes)
        from metrics.tasks.registry import TaskRegistry

        task_count = len(TaskRegistry._tasks)
        self.stdout.write(self.style.SUCCESS(f"Scheduled {task_count} registered tasks"))

        duration = (timezone.now() - start_time).total_seconds()
        self.stdout.write(
            self.style.SUCCESS(f"All startup tasks scheduled in {duration:.2f} seconds")
        )
        self.stdout.write(
            "Note: Tasks are running asynchronously. Check logs for completion status."
        )
