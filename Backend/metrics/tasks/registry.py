"""
Task Observer pattern implementation for scheduled metrics operations.
This module provides a centralized way to register and execute tasks on schedule.
"""
from typing import Dict, List, Callable, Any
from django.utils import timezone
from core.utils.logger import logger


class TaskRegistry:
    """
    Registry for metrics tasks that need to be executed.
    Implements a simplified Observer pattern for task management.
    """
    _tasks: List[Callable] = []

    @classmethod
    def register(cls, task_func: Callable):
        """
        Register a task function to be executed.

        Args:
            task_func: The function to execute

        Returns:
            The original function (for decorator use)
        """
        cls._tasks.append(task_func)
        logger.info(f"Task {task_func.__name__} registered for execution")
        return task_func  # Return the function for use as a decorator

    @classmethod
    def execute_all_tasks(cls) -> Dict[str, Any]:
        """
        Execute all registered tasks.

        Returns:
            Dict containing execution results
        """
        start_time = timezone.now()
        results = {}

        logger.info(f"Executing {len(cls._tasks)} registered tasks")

        for task_func in cls._tasks:
            task_name = task_func.__name__
            try:
                logger.info(f"Executing task: {task_name}")
                result = task_func()
                results[task_name] = {'success': True, 'result': result}
                logger.info(f"Successfully executed task: {task_name}")
            except Exception as e:
                logger.error(f"Error executing task {task_name}: {e}")
                results[task_name] = {'success': False, 'error': str(e)}

        duration = (timezone.now() - start_time).total_seconds()
        logger.info(f"Completed {len(cls._tasks)} tasks in {duration:.2f}s")

        return results

    @classmethod
    def __len__(cls) -> int:
        """Return the number of registered tasks."""
        return len(cls._tasks)

    @classmethod
    def __iter__(cls):
        """Iterate over registered tasks."""
        return iter(cls._tasks)


# Decorator function for easy task registration
def register_task(func):
    """Decorator to register a task for execution with both TaskRegistry and Celery"""
    from celery import shared_task

    # First, register with TaskRegistry
    TaskRegistry.register(func)

    # Then, also register with Celery as a shared task
    celery_task = shared_task(func)

    return celery_task
