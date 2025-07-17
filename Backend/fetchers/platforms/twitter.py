import re

from bs4 import BeautifulSoup

from fetchers.base import BaseFetcher


class TwitterFetcher(BaseFetcher):
    def __init__(self, platform_url):
        self.platform_url = platform_url

    def fetch_followers_count(self):
        page_source = self._get_page_source_with_browser(self.platform_url)
        soup = BeautifulSoup(page_source, "html.parser")

        # Strategy 1: Find links containing "followers" in the href, including "verified_followers"
        follower_link = soup.find(
            "a", href=re.compile(r"/(verified_)?followers", re.IGNORECASE)
        )

        if follower_link:
            # The count is in a span, and the text "Followers" is in another.
            # We'll get all the text and use regex to find the number next to "Followers"
            link_text = follower_link.get_text(separator=" ", strip=True)
            # This regex looks for a number (with commas) that is followed by "Followers"
            match = re.search(r"([\d,]+)\s+Followers", link_text, re.IGNORECASE)
            if match:
                count_text = match.group(1)
                try:
                    return self._parse_count(count_text)
                except ValueError:
                    pass  # Fallback to other strategies if parsing fails

        raise ValueError("Could not find followers count on the page for Twitter.")


if __name__ == "__main__":
    # Example usage:
    twitter_fetcher = TwitterFetcher("https://twitter.com/bloocktecs")
    print(twitter_fetcher.fetch_followers_count())
    pass
