import time

import requests

from src.helper import concurrent_fetch

URL_A = "https://example.test/a"
URL_B = "https://example.test/b"
URL_C = "https://example.test/c"


def test_fetch_all_yields_results_in_input_order(monkeypatch):
    def fake_get(session, url):
        if url == URL_A:
            time.sleep(0.05)
        return f"body-of-{url}"

    monkeypatch.setattr(concurrent_fetch.http_client, "get", fake_get)

    results = list(concurrent_fetch.fetch_all(None, [URL_A, URL_B, URL_C]))

    assert [url for url, _, _ in results] == [URL_A, URL_B, URL_C]
    assert [r for _, r, _ in results] == [f"body-of-{url}" for url in [URL_A, URL_B, URL_C]]
    assert all(error is None for _, _, error in results)


def test_fetch_all_captures_request_exception_instead_of_raising(monkeypatch):
    boom = requests.ConnectionError("boom")

    def fake_get(session, url):
        if url == URL_A:
            raise boom
        return f"body-of-{url}"

    monkeypatch.setattr(concurrent_fetch.http_client, "get", fake_get)

    results = list(concurrent_fetch.fetch_all(None, [URL_A, URL_B]))

    assert results[0] == (URL_A, None, boom)
    assert results[1] == (URL_B, f"body-of-{URL_B}", None)


def test_fetch_all_returns_nothing_for_empty_input():
    results = list(concurrent_fetch.fetch_all(None, []))

    assert results == []


def test_rate_limiter_enforces_minimum_spacing_between_calls():
    limiter = concurrent_fetch.RateLimiter(0.05)

    start = time.monotonic()
    limiter.wait()
    limiter.wait()
    elapsed = time.monotonic() - start

    assert elapsed >= 0.05
