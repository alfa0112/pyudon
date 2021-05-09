import hashlib
from pathlib import Path


class HashMaker():
    def __init__(self, algorithm="sha256"):
        self._algorithm = algorithm

    def make_from_file(self, path: Path) -> str:
        path = Path(path)

        with path.open("rb") as f:
            data = f.read()

        return self.make_from_binary(data)

    def make_from_binary(self, data: bytes):
        hash_obj = hashlib.new(self._algorithm)
        hash_obj.update(data)
        hashed_name = hash_obj.hexdigest()

        return hashed_name

