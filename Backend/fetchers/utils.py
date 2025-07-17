import importlib

from django.core.exceptions import ImproperlyConfigured


def run_fetcher(platform) -> int:
    """
    Given a Platform instance that has fetch_script and page_url,
    import & instantiate the fetcher, call fetch_followers_count(),
    return the int.
    """
    fetch_script = platform.fetch_script
    if not fetch_script:
        raise ImproperlyConfigured(f"No FetchScript linked for {platform.name}")
    module_path, class_name = fetch_script.script_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    FetcherCls = getattr(module, class_name)
    fetcher = FetcherCls(platform.page_url)
    return fetcher.fetch_followers_count()
