import configparser
import csv
from pathlib import Path

import pytest

from src.helper import concurrent_fetch, http_client

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def read_fixture(name):
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


def write_csv(path, values):
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=';', quotechar='|')
        for value in values:
            writer.writerow([value])


def read_csv_rows(path):
    with open(path, newline="", encoding="utf-8") as csv_file:
        return list(csv.reader(csv_file, delimiter=';', quotechar='|'))


class FakeResponse:
    def __init__(self, text):
        self.text = text


@pytest.fixture(autouse=True)
def _fast_concurrent_fetch(monkeypatch):
    monkeypatch.setattr(concurrent_fetch, "MIN_REQUEST_INTERVAL", 0)


@pytest.fixture
def isolated_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Excelfiles").mkdir()
    return tmp_path


@pytest.fixture
def mail_config(isolated_cwd):
    config_dir = isolated_cwd / ".config"
    config_dir.mkdir()
    config = configparser.ConfigParser()
    config["MAILS"] = {
        "mail1": "Sportwart:in",
        "mail2": "Jugendwart:in",
        "mail3": "1. Vorsitzende:r",
        "mail4": "2. Vorsitzende:r",
    }
    with open(config_dir / "config.ini", "w", encoding="utf-8") as config_file:
        config.write(config_file)
    return config_dir / "config.ini"


@pytest.fixture
def patch_http_get(monkeypatch):
    def install(responses):
        def fake_get(session, url):
            if callable(responses):
                result = responses(url)
            elif isinstance(responses, dict):
                result = responses[url]
            else:
                result = responses

            if isinstance(result, BaseException):
                raise result
            return FakeResponse(result)

        monkeypatch.setattr(http_client, "get", fake_get)

    return install
