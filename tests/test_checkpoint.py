from src.helper.checkpoint import Checkpoint


def test_is_done_false_when_checkpoint_file_does_not_exist(tmp_path):
    checkpoint = Checkpoint(tmp_path / "stage.checkpoint")

    assert checkpoint.is_done("https://example.test/a") is False
    checkpoint.close()


def test_mark_done_persists_across_instances(tmp_path):
    path = tmp_path / "stage.checkpoint"
    checkpoint = Checkpoint(path)
    checkpoint.mark_done("https://example.test/a")
    checkpoint.close()

    resumed = Checkpoint(path)

    assert resumed.is_done("https://example.test/a") is True
    assert resumed.is_done("https://example.test/b") is False
    resumed.close()
