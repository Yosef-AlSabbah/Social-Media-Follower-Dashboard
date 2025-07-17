import time
from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class BaseFetcher(ABC):
    @abstractmethod
    def fetch_followers_count(self) -> int: ...

    @staticmethod
    def _parse_count(count_str: str) -> int:
        """Parse count string like '12K' or '1.5M' to integer"""
        count_str = count_str.strip().upper().replace(",", "")

        if count_str.endswith("K"):
            return int(float(count_str[:-1]) * 1000)
        elif count_str.endswith("M"):
            return int(float(count_str[:-1]) * 1000000)
        else:
            # handles cases with only digits
            numeric_part = "".join([c for c in str(count_str) if c.isdigit()])
            if numeric_part:
                return int(numeric_part)

        raise ValueError(f"Unrecognized count: {count_str!r}")

    @staticmethod
    def _get_page_source_with_browser(url: str, user_agent: str = None) -> str:
        """Fetches the page source using a headless browser to handle dynamic content."""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        default_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
        options.add_argument(f"user-agent={user_agent or default_user_agent}")

        options.add_argument("accept-language=en-US,en;q=0.9")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get(url)
            # A generic wait for page to load, can be customized in subclasses if needed
            time.sleep(5)
            return driver.page_source
        finally:
            driver.quit()
