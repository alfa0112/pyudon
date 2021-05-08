import hashlib
from pathlib import Path


class FileToHashMaker():
    def __init__(self, algorithm="sha256"):
        self._algorithm = algorithm

    def make_from_file(self, path: Path) -> str:
        path = Path(path)

        with path.open("rb") as f:
            binary = f.read()

        hash_obj = hashlib.new(self._algorithm)
        hash_obj.update(binary)
        hashed_name = hash_obj.hexdigest()

        return hashed_name

