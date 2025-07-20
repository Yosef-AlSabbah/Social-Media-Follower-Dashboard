from django.apps import AppConfig
from django.db.models.signals import post_migrate


# Global flag to prevent multiple executions
_startup_tasks_executed = False


def trigger_tasks(sender, **kwargs):
    global _startup_tasks_executed

    # Prevent multiple executions
    if _startup_tasks_executed:
        return

    _startup_tasks_executed = True

    # Only import and run tasks after migrations complete
    try:
        from django.core.management import call_command
        call_command('trigger_startup_tasks')
    except Exception as e:
        print(f"Error triggering startup tasks: {e}")


class MetricsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'metrics'

    def ready(self):
        """
        Called when the app is ready. This is where we register our signal handlers.
        """
        # Import signals to register them
        from . import signals

        # Connect the post-migrate signal for startup tasks
        post_migrate.connect(trigger_tasks, sender=self)
