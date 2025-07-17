import re
from bs4 import BeautifulSoup
from fetchers.base import BaseFetcher


class LinkedinFetcher(BaseFetcher):
    def __init__(self, platform_url):
        self.platform_url = platform_url

    def fetch_followers_count(self):
        page_source = self._get_page_source_with_browser(self.platform_url)
        soup = BeautifulSoup(page_source, "html.parser")

        text_elements = soup.find_all(
            string=re.compile(r"[\d,.]+[KM]?\s+followers", re.IGNORECASE)
        )
        for element in text_elements:
            match = re.search(r"([\d,.]+[KM]?)\s+followers", element, re.IGNORECASE)
            if match:
                return self._parse_count(match.group(1))
        raise ValueError("Could not find followers count on the page for LinkedIn.")
