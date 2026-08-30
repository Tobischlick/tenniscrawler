from urllib.parse import urljoin

import requests

from src.crawler.crawled_teams import CrawledTeams
from tests.conftest import read_csv_rows, read_fixture, write_csv

LEAGUE_A_URL = "https://example.test/bezirk/leagueA"
LEAGUE_B_URL = "https://example.test/bezirk/leagueB"
TEAM_HREFS = ["clubPage?club=1", "clubPage?club=2"]


def test_fetch_writes_links_for_every_input_row(isolated_cwd, patch_http_get):
    input_path = isolated_cwd / "leagues.csv"
    write_csv(input_path, [LEAGUE_A_URL, LEAGUE_B_URL])
    team_page_html = read_fixture("team_page.html")
    patch_http_get({LEAGUE_A_URL: team_page_html, LEAGUE_B_URL: team_page_html})

    filename = CrawledTeams(str(input_path), session=None).fetch(1)

    assert filename == "./Excelfiles/02_Mannschaften_Bezirk_1.csv"
    rows = read_csv_rows(isolated_cwd / "Excelfiles" / "02_Mannschaften_Bezirk_1.csv")
    expected = [[urljoin(LEAGUE_A_URL, href)] for href in TEAM_HREFS]
    expected += [[urljoin(LEAGUE_B_URL, href)] for href in TEAM_HREFS]
    assert rows == expected


def test_fetch_skips_row_on_request_exception(isolated_cwd, patch_http_get):
    input_path = isolated_cwd / "leagues.csv"
    write_csv(input_path, [LEAGUE_A_URL, LEAGUE_B_URL])
    team_page_html = read_fixture("team_page.html")

    def responses(url):
        if url == LEAGUE_A_URL:
            raise requests.ConnectionError("boom")
        return team_page_html

    patch_http_get(responses)

    CrawledTeams(str(input_path), session=None).fetch(1)

    rows = read_csv_rows(isolated_cwd / "Excelfiles" / "02_Mannschaften_Bezirk_1.csv")
    assert rows == [[urljoin(LEAGUE_B_URL, href)] for href in TEAM_HREFS]


def test_fetch_skips_row_missing_result_set(isolated_cwd, patch_http_get):
    input_path = isolated_cwd / "leagues.csv"
    write_csv(input_path, [LEAGUE_A_URL, LEAGUE_B_URL])
    patch_http_get({
        LEAGUE_A_URL: read_fixture("no_result_set.html"),
        LEAGUE_B_URL: read_fixture("team_page.html"),
    })

    CrawledTeams(str(input_path), session=None).fetch(1)

    rows = read_csv_rows(isolated_cwd / "Excelfiles" / "02_Mannschaften_Bezirk_1.csv")
    assert rows == [[urljoin(LEAGUE_B_URL, href)] for href in TEAM_HREFS]


def test_fetch_skips_if_output_already_exists(isolated_cwd):
    input_path = isolated_cwd / "leagues.csv"
    write_csv(input_path, [LEAGUE_A_URL])
    output_path = isolated_cwd / "Excelfiles" / "02_Mannschaften_Bezirk_1.csv"
    output_path.write_text("SENTINEL\n", encoding="utf-8")

    CrawledTeams(str(input_path), session=None).fetch(1)

    assert output_path.read_text(encoding="utf-8") == "SENTINEL\n"
