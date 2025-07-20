from django.core.management.base import BaseCommand
from django.utils import timezone

from core.utils.logger import logger
from metrics.models import Platform


class Command(BaseCommand):
    help = 'Diagnose platform configuration and test metric fetching'

    def add_arguments(self, parser):
        parser.add_argument(
            '--platform',
            type=str,
            help='Test specific platform by name',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output',
        )

    def handle(self, *args, **options):
        platform_name = options.get('platform')
        verbose = options.get('verbose', False)

        self.stdout.write(self.style.SUCCESS("🔍 Platform Diagnostics Starting..."))

        # Get platforms to test
        if platform_name:
            platforms = Platform.objects.filter(name__icontains=platform_name)
            if not platforms.exists():
                self.stdout.write(
                    self.style.ERROR(f"No platform found matching '{platform_name}'")
                )
                return
        else:
            platforms = Platform.objects.all()

        if not platforms.exists():
            self.stdout.write(self.style.ERROR("No platforms found in database"))
            return

        self.stdout.write(f"Testing {platforms.count()} platform(s)...")

        for platform in platforms:
            self.test_platform(platform, verbose)

    def test_platform(self, platform, verbose=False):
        """Test a single platform's configuration and fetching capability"""

        self.stdout.write(f"\n{'='*50}")
        self.stdout.write(f"🧪 Testing Platform: {platform.name}")
        self.stdout.write(f"{'='*50}")

        # Test 1: Basic Configuration
        self.stdout.write("📋 Configuration Check:")

        if not platform.page_url:
            self.stdout.write(self.style.ERROR("  ✗ Missing page_url"))
        else:
            self.stdout.write(f"  ✓ Page URL: {platform.page_url}")

        if not platform.fetch_script:
            self.stdout.write(self.style.ERROR("  ✗ Missing fetch_script"))
        else:
            self.stdout.write(f"  ✓ Fetch Script: {platform.fetch_script.name}")
            if verbose:
                self.stdout.write(f"    Script Path: {platform.fetch_script.script_path}")

        self.stdout.write(f"  ✓ Active: {platform.is_active}")
        self.stdout.write(f"  ✓ Color: {platform.color}")

        # Test 2: Fetcher Import Test
        self.stdout.write("\n🔌 Fetcher Import Test:")

        if not platform.fetch_script:
            self.stdout.write(self.style.ERROR("  ✗ Cannot test - no fetch script configured"))
            return

        try:
            # Try to import the fetcher class
            script_path = platform.fetch_script.script_path
            module_path, class_name = script_path.rsplit('.', 1)

            import importlib
            module = importlib.import_module(module_path)
            fetcher_class = getattr(module, class_name)

            self.stdout.write(f"  ✓ Successfully imported {class_name}")

            # Test 3: Fetcher Instantiation
            self.stdout.write("\n🏗️ Fetcher Instantiation Test:")

            if not platform.page_url:
                self.stdout.write(self.style.ERROR("  ✗ Cannot instantiate - no page_url"))
            else:
                fetcher_instance = fetcher_class(platform.page_url)
                self.stdout.write(f"  ✓ Successfully created fetcher instance")

                # Test 4: Metrics Refresh (Dry Run)
                self.stdout.write("\n📊 Metrics Refresh Test:")

                try:
                    start_time = timezone.now()
                    success = platform.refresh_metrics()
                    duration = (timezone.now() - start_time).total_seconds()

                    if success:
                        self.stdout.write(
                            self.style.SUCCESS(f"  ✓ Metrics refresh successful ({duration:.2f}s)")
                        )

                        # Show current metrics
                        self.stdout.write(f"  📈 Current Followers: {platform.followers}")
                        self.stdout.write(f"  📊 Delta: {platform.delta}")
                        self.stdout.write(f"  🕒 Last Updated: {platform.last_updated}")

                    else:
                        self.stdout.write(
                            self.style.ERROR(f"  ✗ Metrics refresh failed ({duration:.2f}s)")
                        )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"  ✗ Metrics refresh error: {e}")
                    )
                    if verbose:
                        import traceback
                        self.stdout.write(traceback.format_exc())

        except ImportError as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Import failed: {e}"))
        except AttributeError as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Class not found: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Unexpected error: {e}"))
            if verbose:
                import traceback
                self.stdout.write(traceback.format_exc())

        # Test 5: Cache Check
        self.stdout.write("\n💾 Cache Check:")

        try:
            from core.utils.platform_cache import PlatformCacheManager

            followers = PlatformCacheManager.get_followers(platform.name)
            delta = PlatformCacheManager.get_delta(platform.name)
            last_updated = PlatformCacheManager.get_last_updated(platform.name)

            self.stdout.write(f"  📈 Cached Followers: {followers}")
            self.stdout.write(f"  📊 Cached Delta: {delta}")
            self.stdout.write(f"  🕒 Cached Last Updated: {last_updated}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Cache error: {e}"))
