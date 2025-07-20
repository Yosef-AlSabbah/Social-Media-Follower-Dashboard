import os
import importlib
import inspect
from django.core.management.base import BaseCommand
from django.db import transaction

from metrics.models import FetchScript
from fetchers.base import BaseFetcher


class Command(BaseCommand):
    help = 'Automatically populate FetchScript entries for all available fetchers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating the entries',
        )

    def discover_fetchers(self):
        """Dynamically discover all fetcher classes from fetchers.platforms module"""
        fetchers = []

        try:
            # Import the platforms module
            platforms_module = importlib.import_module('fetchers.platforms')

            # Get all exported classes from __all__
            if hasattr(platforms_module, '__all__'):
                for class_name in platforms_module.__all__:
                    try:
                        # Get the actual class from the module
                        fetcher_class = getattr(platforms_module, class_name)

                        # Verify it's a subclass of BaseFetcher
                        if (inspect.isclass(fetcher_class) and
                            issubclass(fetcher_class, BaseFetcher) and
                            fetcher_class != BaseFetcher):

                            # Generate human-friendly name from class name
                            # e.g., "FacebookFetcher" -> "Facebook Fetcher"
                            name = fetcher_class.__name__.replace('Fetcher', ' Fetcher')
                            if not name.endswith(' Fetcher'):
                                name += ' Fetcher'

                            # Generate script path
                            module_name = fetcher_class.__module__
                            script_path = f"{module_name}.{fetcher_class.__name__}"

                            fetchers.append({
                                'name': name,
                                'script_path': script_path,
                                'class_name': fetcher_class.__name__
                            })

                    except (AttributeError, ImportError) as e:
                        self.stdout.write(
                            self.style.WARNING(f"Could not load class '{class_name}': {e}")
                        )

            # Sort by name for consistent output
            fetchers.sort(key=lambda x: x['name'])

        except ImportError as e:
            self.stdout.write(
                self.style.ERROR(f"Could not import fetchers.platforms module: {e}")
            )

        return fetchers

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        created_count = 0
        existing_count = 0

        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made')
            )

        # Dynamically discover all fetchers
        self.stdout.write("Discovering available fetchers...")
        fetchers = self.discover_fetchers()

        if not fetchers:
            self.stdout.write(
                self.style.WARNING("No fetchers found in fetchers.platforms module")
            )
            return

        self.stdout.write(f"Found {len(fetchers)} fetcher(s):")
        for fetcher in fetchers:
            self.stdout.write(f"  - {fetcher['name']} ({fetcher['class_name']})")

        with transaction.atomic():
            for fetcher_info in fetchers:
                name = fetcher_info['name']
                script_path = fetcher_info['script_path']

                # Check if the fetch script already exists
                if FetchScript.objects.filter(name=name).exists():
                    existing_count += 1
                    self.stdout.write(
                        f"✓ FetchScript '{name}' already exists"
                    )
                else:
                    if not dry_run:
                        # Create the new FetchScript entry
                        FetchScript.objects.create(
                            name=name,
                            script_path=script_path
                        )
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"✓ Created FetchScript '{name}'")
                        )
                    else:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"Would create FetchScript '{name}'")
                        )

        # Summary
        self.stdout.write("\n" + "="*50)
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f"DRY RUN SUMMARY:")
            )
            self.stdout.write(f"Would create: {created_count} new FetchScript entries")
        else:
            self.stdout.write(
                self.style.SUCCESS(f"OPERATION COMPLETED:")
            )
            self.stdout.write(f"Created: {created_count} new FetchScript entries")

        self.stdout.write(f"Already existing: {existing_count} FetchScript entries")
        self.stdout.write(f"Total fetchers available: {len(fetchers)}")
