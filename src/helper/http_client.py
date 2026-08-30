import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 15
USER_AGENT = "TennisCrawlerBot/1.0 (+https://github.com/Tobischlick/tenniscrawler)"


def create_session():
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get(session, url):
    response = session.get(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response
