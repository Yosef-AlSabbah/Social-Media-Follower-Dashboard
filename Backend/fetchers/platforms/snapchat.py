from fetchers.base import BaseFetcher


class SnapchatFetcher(BaseFetcher):
    def __init__(self, platform_url):
        self.platform_url = platform_url

    def fetch_followers_count(self):
        # FUTURE: Implement actual fetching logic for Snapchat
        return 3670


if __name__ == "__main__":
    fetcher = SnapchatFetcher("https://www.snapchat.com/add/bloocktecs")
    print(f"Snapchat Subscribers: {fetcher.fetch_followers_count()}")
