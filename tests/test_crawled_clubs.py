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


def test_fetch_skips_row_when_result_set_has_no_links(isolated_cwd, patch_http_get):
    input_path = isolated_cwd / "clubs.csv"
    write_csv(input_path, [CLUB_A_URL, CLUB_B_URL])
    patch_http_get({
        CLUB_A_URL: read_fixture("club_page_empty_links.html"),
        CLUB_B_URL: read_fixture("club_page.html"),
    })

    CrawledClubs(str(input_path), session=None).fetch(1)

    rows = read_csv_rows(isolated_cwd / "Excelfiles" / "03_Clubs_Bezirk_1.csv")
    assert rows == [[CLUB_SITE_URL]]


def test_fetch_resumes_and_skips_already_checkpointed_rows(isolated_cwd, patch_http_get):
    input_path = isolated_cwd / "clubs.csv"
    write_csv(input_path, [CLUB_A_URL, CLUB_B_URL])
    output_path = isolated_cwd / "Excelfiles" / "03_Clubs_Bezirk_1.csv"
    write_csv(output_path, [CLUB_SITE_URL])
    (isolated_cwd / "Excelfiles" / "03_Clubs_Bezirk_1.csv.checkpoint").write_text(
        CLUB_A_URL + "\n", encoding="utf-8")

    def responses(url):
        if url == CLUB_A_URL:
            raise AssertionError("already-checkpointed row should not be refetched")
        return read_fixture("club_page.html")

    patch_http_get(responses)

    CrawledClubs(str(input_path), session=None).fetch(1)

    rows = read_csv_rows(output_path)
    assert rows == [[CLUB_SITE_URL], [CLUB_SITE_URL]]
