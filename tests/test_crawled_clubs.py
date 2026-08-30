import pytest
import requests

from src.crawler.crawled_clubs import CrawledClubs
from tests.conftest import read_csv_rows, read_fixture, write_csv

CLUB_A_URL = "https://example.test/bezirk/clubListingA"
CLUB_B_URL = "https://example.test/bezirk/clubListingB"
CLUB_SITE_URL = "https://tc-beispiel.example/"


def test_fetch_writes_first_link_per_row(isolated_cwd, patch_http_get):
    input_path = isolated_cwd / "clubs.csv"
    write_csv(input_path, [CLUB_A_URL, CLUB_B_URL])
    patch_http_get(read_fixture("club_page.html"))

    filename = CrawledClubs(str(input_path), session=None).fetch(1)

    assert filename == "./Excelfiles/03_Clubs_Bezirk_1.csv"
    rows = read_csv_rows(isolated_cwd / "Excelfiles" / "03_Clubs_Bezirk_1.csv")
    assert rows == [[CLUB_SITE_URL], [CLUB_SITE_URL]]


def test_fetch_skips_row_on_request_exception(isolated_cwd, patch_http_get):
    input_path = isolated_cwd / "clubs.csv"
    write_csv(input_path, [CLUB_A_URL, CLUB_B_URL])
    club_page_html = read_fixture("club_page.html")

    def responses(url):
        if url == CLUB_A_URL:
            raise requests.ConnectionError("boom")
        return club_page_html

    patch_http_get(responses)

    CrawledClubs(str(input_path), session=None).fetch(1)

    rows = read_csv_rows(isolated_cwd / "Excelfiles" / "03_Clubs_Bezirk_1.csv")
    assert rows == [[CLUB_SITE_URL]]


def test_fetch_skips_row_missing_result_set(isolated_cwd, patch_http_get):
    input_path = isolated_cwd / "clubs.csv"
    write_csv(input_path, [CLUB_A_URL, CLUB_B_URL])
    patch_http_get({
        CLUB_A_URL: read_fixture("no_result_set.html"),
        CLUB_B_URL: read_fixture("club_page.html"),
    })

    CrawledClubs(str(input_path), session=None).fetch(1)

    rows = read_csv_rows(isolated_cwd / "Excelfiles" / "03_Clubs_Bezirk_1.csv")
    assert rows == [[CLUB_SITE_URL]]


def test_fetch_raises_indexerror_when_result_set_has_no_links(isolated_cwd, patch_http_get):
    input_path = isolated_cwd / "clubs.csv"
    write_csv(input_path, [CLUB_A_URL])
    patch_http_get(read_fixture("club_page_empty_links.html"))

    with pytest.raises(IndexError):
        CrawledClubs(str(input_path), session=None).fetch(1)


def test_fetch_skips_if_output_already_exists(isolated_cwd):
    input_path = isolated_cwd / "clubs.csv"
    write_csv(input_path, [CLUB_A_URL])
    output_path = isolated_cwd / "Excelfiles" / "03_Clubs_Bezirk_1.csv"
    output_path.write_text("SENTINEL\n", encoding="utf-8")

    CrawledClubs(str(input_path), session=None).fetch(1)

    assert output_path.read_text(encoding="utf-8") == "SENTINEL\n"
