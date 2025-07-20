import re

from bs4 import BeautifulSoup

from fetchers.base import BaseFetcher


class TwitterFetcher(BaseFetcher):
    """Fetcher for Twitter/X platform to extract follower counts."""

    def __init__(self, platform_url: str):
        """Initialize the Twitter fetcher with the profile URL.

        Args:
            platform_url: The URL of the Twitter profile
        """
        self.platform_url = platform_url

    def fetch_followers_count(self) -> int:
        """Fetch the follower count from a Twitter profile page.

        Returns:
            The number of followers as an integer

        Raises:
            ValueError: If the followers count cannot be found or parsed
        """
        page_source = self._get_page_source_with_browser(self.platform_url)
        soup = BeautifulSoup(page_source, "html.parser")

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
                    # Fallback to other strategies if parsing fails
                    pass

        # Try alternative approach if the above method failed
        follower_count_element = soup.select_one('[data-testid="followersCount"]')
        if follower_count_element:
            try:
                return self._parse_count(follower_count_element.get_text(strip=True))
            except ValueError:
                pass

        raise ValueError("Could not find followers count on the page for Twitter.")
#
#
# if __name__ == "__main__":
#     # Example usage:
#     try:
#         twitter_fetcher = TwitterFetcher("https://twitter.com/bloocktecs")
#         follower_count = twitter_fetcher.fetch_followers_count()
#         print(f"Follower count: {follower_count}")
#     except Exception as e:
#         print(f"Error fetching follower count: {e}")
