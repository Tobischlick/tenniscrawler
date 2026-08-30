import os
from pathlib import Path


class Checkpoint:
    """Tracks which source rows a crawler stage has already processed, keyed
    by a sidecar file next to the stage's output, so a crashed run can
    resume without reprocessing or duplicating rows."""

    def __init__(self, path):
        self.path = Path(path)
        self.done = self._load()
        self._file = open(self.path, "a", encoding="utf-8")

    def _load(self):
        if not self.path.is_file():
            return set()
        with open(self.path, encoding="utf-8") as f:
            return {line.rstrip("\n") for line in f if line.strip()}

    def is_done(self, key):
        return key in self.done

    def mark_done(self, key):
        self._file.write(key + "\n")
        self._file.flush()
        os.fsync(self._file.fileno())
        self.done.add(key)

    def close(self):
        self._file.close()
