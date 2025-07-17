import re

from bs4 import BeautifulSoup

from fetchers.base import BaseFetcher


class YoutubeFetcher(BaseFetcher):
    def __init__(self, platform_url):
        self.platform_url = platform_url

    def fetch_followers_count(self):
        page_source = self._get_page_source_with_browser(self.platform_url)
        soup = BeautifulSoup(page_source, "html.parser")

        # Strategy 1: Find span tags with "subscribers" in their text
        subscriber_spans = soup.find_all(
            "span", string=re.compile(r"subscribers", re.IGNORECASE)
        )
        for span in subscriber_spans:
            text = span.get_text(strip=True)
            match = re.search(r"([\d,.]+[KM]?)\s+subscribers", text, re.IGNORECASE)
            if match:
                return self._parse_count(match.group(1))

        raise ValueError("Could not find subscriber count on the page for YouTube.")
