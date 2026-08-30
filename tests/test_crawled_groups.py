from urllib.parse import urljoin

import pytest

from src.crawler.crawled_groups import CrawledGroups
from tests.conftest import read_csv_rows, read_fixture

LEAGUE_URL = "https://example.test/leaguePage"
TEAM_HREFS = ["teamPage?team=1", "teamPage?team=2"]


def test_fetch_writes_resolved_links_from_result_set(isolated_cwd, patch_http_get):
    patch_http_get(read_fixture("league_page.html"))

    filename = CrawledGroups(LEAGUE_URL, session=None).fetch(1)

    assert filename == "./Excelfiles/01_Gruppen_Bezirk_1.csv"
    rows = read_csv_rows(isolated_cwd / "Excelfiles" / "01_Gruppen_Bezirk_1.csv")
    assert rows == [[urljoin(LEAGUE_URL, href)] for href in TEAM_HREFS]


def test_fetch_resumes_without_duplicating_already_written_links(isolated_cwd, patch_http_get):
    patch_http_get(read_fixture("league_page.html"))
    output_path = isolated_cwd / "Excelfiles" / "01_Gruppen_Bezirk_1.csv"
    already_written = urljoin(LEAGUE_URL, TEAM_HREFS[0])
    output_path.write_text(f"{already_written}\n", encoding="utf-8")

    CrawledGroups(LEAGUE_URL, session=None).fetch(1)

    rows = read_csv_rows(output_path)
    assert rows == [[urljoin(LEAGUE_URL, href)] for href in TEAM_HREFS]


def test_fetch_raises_when_result_set_is_missing(isolated_cwd, patch_http_get):
    patch_http_get(read_fixture("no_result_set.html"))

    with pytest.raises(AttributeError):
        CrawledGroups(LEAGUE_URL, session=None).fetch(1)
