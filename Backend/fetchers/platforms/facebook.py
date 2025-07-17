import re

from bs4 import BeautifulSoup

from fetchers.base import BaseFetcher


class FacebookFetcher(BaseFetcher):
    def __init__(self, url: str):
        self.platform_url = url

    def fetch_followers_count(self) -> int:
        page_source = self._get_page_source_with_browser(self.platform_url)
        soup = BeautifulSoup(page_source, "html.parser")

        # Look for the followers link pattern
        followers_links = soup.find_all("a", href=re.compile(r"/followers/?$"))

        for link in followers_links:
            text = link.get_text(strip=True)
            match = re.search(r"([\d,.]+[KM]?)\s+followers", text, re.IGNORECASE)
            if match:
                return self._parse_count(match.group(1))

        # Fallback to searching for the strong tag if the above fails
        for link in followers_links:
            strong_tag = link.find("strong")
            if strong_tag:
                followers_text = strong_tag.get_text().strip()
                return self._parse_count(followers_text)

        # Fallback for pages with different structures
        text_elements = soup.find_all(
            string=re.compile(r"[\d,.]+[KM]?\s+followers", re.IGNORECASE)
        )
        for element in text_elements:
            match = re.search(r"([\d,.]+[KM]?)\s+followers", element, re.IGNORECASE)
            if match:
                return self._parse_count(match.group(1))

        raise ValueError("Could not find followers count on the page")
