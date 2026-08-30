import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from src.helper import http_client

logger = logging.getLogger(__name__)

MAX_WORKERS = 4
MIN_REQUEST_INTERVAL = 0.5  # seconds between request starts, shared across all workers


class RateLimiter:
    """Ensures at least `min_interval` seconds pass between request starts, across threads."""

    def __init__(self, min_interval):
        self.min_interval = min_interval
        self.lock = threading.Lock()
        self.last_call = 0.0

    def wait(self):
        with self.lock:
            now = time.monotonic()
            remaining = self.last_call + self.min_interval - now
            if remaining > 0:
                time.sleep(remaining)
            self.last_call = time.monotonic()


def fetch_all(session, urls, max_workers=None, min_interval=None):
    """Fetches `urls` concurrently, yielding (url, response, error) in the same
    order as `urls`. `error` is the caught RequestException, or None on success."""
    if not urls:
        return
    if max_workers is None:
        max_workers = MAX_WORKERS
    if min_interval is None:
        min_interval = MIN_REQUEST_INTERVAL
    limiter = RateLimiter(min_interval)

    def _fetch(url):
        limiter.wait()
        try:
            return url, http_client.get(session, url), None
        except requests.RequestException as e:
            return url, None, e

    with ThreadPoolExecutor(max_workers=min(max_workers, len(urls))) as executor:
        yield from executor.map(_fetch, urls)
