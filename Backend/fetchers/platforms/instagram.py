import requests

from fetchers.base import BaseFetcher


class InstagramFetcher(BaseFetcher):
    def __init__(self, url: str):
        self.platform_url = url

    def fetch_followers_count(self) -> int:
        username = self.platform_url.rstrip("/").split("/")[-1]
        api = (
            f"https://i.instagram.com/api/v1/users/web_profile_info/"
            f"?username={username}"
        )
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0 Safari/537.36"
            ),
            "x-ig-app-id": "936619743392459",
        }
        r = requests.get(api, headers=headers)
        r.raise_for_status()
        data = r.json()
        return data["data"]["user"]["edge_followed_by"]["count"]
