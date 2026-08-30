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


def test_fetch_skips_write_if_output_already_exists(isolated_cwd, patch_http_get):
    patch_http_get(read_fixture("league_page.html"))
    output_path = isolated_cwd / "Excelfiles" / "01_Gruppen_Bezirk_1.csv"
    output_path.write_text("SENTINEL\n", encoding="utf-8")

    CrawledGroups(LEAGUE_URL, session=None).fetch(1)

    assert output_path.read_text(encoding="utf-8") == "SENTINEL\n"


def test_fetch_raises_when_result_set_is_missing(isolated_cwd, patch_http_get):
    patch_http_get(read_fixture("no_result_set.html"))

    with pytest.raises(AttributeError):
        CrawledGroups(LEAGUE_URL, session=None).fetch(1)
