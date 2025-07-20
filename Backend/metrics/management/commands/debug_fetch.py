from django.core.management.base import BaseCommand
from django.utils import timezone
import traceback
import sys
import os

from core.utils.logger import logger
from metrics.models import Platform


class Command(BaseCommand):
    help = 'Detailed diagnostics with comprehensive logging for platform fetching'

    def add_arguments(self, parser):
        parser.add_argument(
            '--platform',
            type=str,
            help='Test specific platform by name',
        )
        parser.add_argument(
            '--test-browser',
            action='store_true',
            help='Test browser environment setup',
        )

    def handle(self, *args, **options):
        platform_name = options.get('platform')
        test_browser = options.get('test_browser', False)

        self.stdout.write(self.style.SUCCESS("🔍 DETAILED Platform Diagnostics Starting..."))

        # Test browser environment first
        if test_browser:
            self.test_browser_environment()
            return

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

        self.stdout.write(f"Testing {platforms.count()} platform(s) with detailed logging...")

        for platform in platforms:
            self.test_platform_detailed(platform)

    def test_browser_environment(self):
        """Test browser and ChromeDriver setup"""

        self.stdout.write(f"\n{'='*60}")
        self.stdout.write("🌐 BROWSER ENVIRONMENT TEST")
        self.stdout.write(f"{'='*60}")

        # Test 1: Check Chrome installation
        self.stdout.write("\n1️⃣ Testing Chrome Installation:")
        try:
            import subprocess
            result = subprocess.run(['google-chrome', '--version'],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Chrome installed: {result.stdout.strip()}"))
            else:
                self.stdout.write(self.style.ERROR(f"  ✗ Chrome not working: {result.stderr}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Chrome test failed: {e}"))

        # Test 2: Test Selenium WebDriver setup
        self.stdout.write("\n2️⃣ Testing Selenium WebDriver:")
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager

            self.stdout.write("  📦 Setting up Chrome options...")
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')

            self.stdout.write("  🚀 Installing ChromeDriver...")
            service = Service(ChromeDriverManager().install())

            self.stdout.write("  🌐 Creating WebDriver instance...")
            driver = webdriver.Chrome(service=service, options=options)

            self.stdout.write("  🔗 Testing navigation...")
            driver.get("https://www.google.com")
            title = driver.title

            driver.quit()

            self.stdout.write(self.style.SUCCESS(f"  ✓ WebDriver test successful! Page title: {title}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ WebDriver test failed: {e}"))
            self.stdout.write("  📋 Full traceback:")
            self.stdout.write(traceback.format_exc())

    def test_platform_detailed(self, platform):
        """Test a single platform with comprehensive logging"""

        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(f"🧪 DETAILED TESTING: {platform.name}")
        self.stdout.write(f"{'='*60}")

        # Basic configuration check
        self.stdout.write("📋 Configuration Details:")
        self.stdout.write(f"  • Platform ID: {platform.id}")
        self.stdout.write(f"  • Name: {platform.name}")
        self.stdout.write(f"  • Arabic Name: {platform.name_ar}")
        self.stdout.write(f"  • Page URL: {platform.page_url}")
        self.stdout.write(f"  • Active: {platform.is_active}")
        self.stdout.write(f"  • Color: {platform.color}")

        if platform.fetch_script:
            self.stdout.write(f"  • Fetch Script: {platform.fetch_script.name}")
            self.stdout.write(f"  • Script Path: {platform.fetch_script.script_path}")
        else:
            self.stdout.write(self.style.ERROR("  ✗ No fetch script configured"))
            return

        # Test fetcher import and setup
        self.stdout.write("\n🔌 Fetcher Setup Test:")
        try:
            script_path = platform.fetch_script.script_path
            module_path, class_name = script_path.rsplit('.', 1)

            self.stdout.write(f"  📦 Importing from: {module_path}")
            self.stdout.write(f"  🎯 Class name: {class_name}")

            import importlib
            module = importlib.import_module(module_path)
            fetcher_class = getattr(module, class_name)

            self.stdout.write("  ✓ Fetcher class imported successfully")

            # Test instantiation
            self.stdout.write(f"  🏗️ Creating fetcher with URL: {platform.page_url}")
            fetcher_instance = fetcher_class(platform.page_url)
            self.stdout.write("  ✓ Fetcher instance created successfully")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Fetcher setup failed: {e}"))
            self.stdout.write("  📋 Full traceback:")
            self.stdout.write(traceback.format_exc())
            return

        # Test the actual fetching process with detailed logging
        self.stdout.write("\n📊 DETAILED FETCHING TEST:")
        self.stdout.write("  🚀 Starting metrics refresh...")

        try:
            # Import the run_fetcher function
            from fetchers import run_fetcher

            self.stdout.write("  📋 About to call run_fetcher...")
            self.stdout.write(f"  🎯 Platform: {platform.name}")
            self.stdout.write(f"  🔗 URL: {platform.page_url}")

            start_time = timezone.now()

            # Call the fetcher with logging
            self.stdout.write("  ⏳ Executing fetcher...")

            try:
                result = run_fetcher(platform)
                duration = (timezone.now() - start_time).total_seconds()

                if result:
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✓ Fetching successful! Result: {result} followers ({duration:.2f}s)")
                    )

                    # Test cache update
                    self.stdout.write("  💾 Testing cache update...")
                    from core.utils.platform_cache import PlatformCacheManager

                    try:
                        PlatformCacheManager.update_platform_metrics(platform.name, result)
                        self.stdout.write("  ✓ Cache updated successfully")

                        # Verify cache
                        cached_followers = PlatformCacheManager.get_followers(platform.name)
                        cached_delta = PlatformCacheManager.get_delta(platform.name)
                        cached_updated = PlatformCacheManager.get_last_updated(platform.name)

                        self.stdout.write(f"  📈 Cached Followers: {cached_followers}")
                        self.stdout.write(f"  📊 Cached Delta: {cached_delta}")
                        self.stdout.write(f"  🕒 Last Updated: {cached_updated}")

                    except Exception as cache_error:
                        self.stdout.write(self.style.ERROR(f"  ✗ Cache update failed: {cache_error}"))

                else:
                    self.stdout.write(
                        self.style.ERROR(f"  ✗ Fetching returned no result ({duration:.2f}s)")
                    )

            except Exception as fetch_error:
                duration = (timezone.now() - start_time).total_seconds()
                self.stdout.write(
                    self.style.ERROR(f"  ✗ Fetching failed: {fetch_error} ({duration:.2f}s)")
                )
                self.stdout.write("  📋 Fetch error traceback:")
                self.stdout.write(traceback.format_exc())

        except ImportError as import_error:
            self.stdout.write(self.style.ERROR(f"  ✗ Could not import run_fetcher: {import_error}"))
        except Exception as general_error:
            self.stdout.write(self.style.ERROR(f"  ✗ Unexpected error: {general_error}"))
            self.stdout.write("  📋 Full traceback:")
            self.stdout.write(traceback.format_exc())

        # Environment information
        self.stdout.write("\n🔧 Environment Information:")
        self.stdout.write(f"  • Python version: {sys.version}")
        self.stdout.write(f"  • Working directory: {os.getcwd()}")
        self.stdout.write(f"  • PATH: {os.environ.get('PATH', 'Not found')[:100]}...")

        # Check for Chrome in PATH
        try:
            import subprocess
            result = subprocess.run(['which', 'google-chrome'],
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.stdout.write(f"  • Chrome location: {result.stdout.strip()}")
            else:
                self.stdout.write("  • Chrome not found in PATH")
        except:
            self.stdout.write("  • Could not check Chrome location")
