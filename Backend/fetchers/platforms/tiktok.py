from bs4 import BeautifulSoup
from fetchers.base import BaseFetcher


class TiktokFetcher(BaseFetcher):
    def __init__(self, platform_url):
        self.platform_url = platform_url

    def fetch_followers_count(self):
        page_source = self._get_page_source_with_browser(self.platform_url)
        soup = BeautifulSoup(page_source, "html.parser")

        followers_strong = soup.find("strong", {"data-e2e": "followers-count"})

        if followers_strong:
            followers_text = followers_strong.text.strip()
            return self._parse_count(followers_text)

        return 0
