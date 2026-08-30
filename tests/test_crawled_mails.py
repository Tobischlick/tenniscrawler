import pytest
import requests

from src.crawler.crawled_mails import CrawledMails
from tests.conftest import read_csv_rows, read_fixture, write_csv

CLUB_SITE_A_URL = "https://tc-beispiel-a.example/"
CLUB_SITE_B_URL = "https://tc-beispiel-b.example/"


def test_fetch_extracts_configured_mails_and_skips_placeholder(isolated_cwd, mail_config, patch_http_get):
    input_path = isolated_cwd / "clubsites.csv"
    write_csv(input_path, [CLUB_SITE_A_URL])
    patch_http_get(read_fixture("club_site_mails.html"))
    filename_mails = "./Excelfiles/04_Mails.csv"

    CrawledMails(str(input_path), session=None).fetch(1, filename_mails)

    rows = read_csv_rows(isolated_cwd / "Excelfiles" / "04_Mails.csv")
    assert rows == [
        ["Position", "E-Mail", "Bezirk"],
        ["Sportwart:in", "max.mustermann@tvbeispiel.de", "1"],
        ["Jugendwart:in", "info@tvbeispiel.de", "1"],
    ]


def test_fetch_skips_row_on_request_exception(isolated_cwd, mail_config, patch_http_get):
    input_path = isolated_cwd / "clubsites.csv"
    write_csv(input_path, [CLUB_SITE_A_URL, CLUB_SITE_B_URL])
    club_site_html = read_fixture("club_site_mails.html")

    def responses(url):
        if url == CLUB_SITE_A_URL:
            raise requests.ConnectionError("boom")
        return club_site_html

    patch_http_get(responses)
    filename_mails = "./Excelfiles/04_Mails.csv"

    CrawledMails(str(input_path), session=None).fetch(1, filename_mails)

    rows = read_csv_rows(isolated_cwd / "Excelfiles" / "04_Mails.csv")
    assert rows == [
        ["Position", "E-Mail", "Bezirk"],
        ["Sportwart:in", "max.mustermann@tvbeispiel.de", "1"],
        ["Jugendwart:in", "info@tvbeispiel.de", "1"],
    ]


def test_encode_mail_with_two_name_parts():
    crawled_mails = CrawledMails(filepath="unused", session=None)

    result = crawled_mails.encode_mail("encodeEmail('de', 'max', 'tvbeispiel', 'mustermann')")

    assert result == "max.mustermann@tvbeispiel.de"


def test_encode_mail_with_single_name_part():
    crawled_mails = CrawledMails(filepath="unused", session=None)

    result = crawled_mails.encode_mail("encodeEmail('de', 'info', 'tvbeispiel', '')")

    assert result == "info@tvbeispiel.de"


def test_encode_mail_raises_on_malformed_payload():
    crawled_mails = CrawledMails(filepath="unused", session=None)

    with pytest.raises(IndexError):
        crawled_mails.encode_mail("encodeEmail('de', 'info', 'tvbeispiel')")
