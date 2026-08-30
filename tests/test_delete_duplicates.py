from src.helper.delete_duplicates import DeleteDuplicates
from tests.conftest import read_csv_rows, write_csv


def test_delete_removes_duplicates_preserving_order(tmp_path):
    path = tmp_path / "data.csv"
    write_csv(path, ["a", "b", "a", "c", "b"])

    DeleteDuplicates().delete(str(path))

    assert read_csv_rows(path) == [["a"], ["b"], ["c"]]


def test_delete_leaves_file_untouched_when_no_duplicates(tmp_path):
    path = tmp_path / "data.csv"
    write_csv(path, ["a", "b", "c"])
    original_content = path.read_text(encoding="utf-8")

    DeleteDuplicates().delete(str(path))

    assert path.read_text(encoding="utf-8") == original_content
