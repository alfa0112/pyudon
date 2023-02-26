import hashlib
import zipfile
from pathlib import Path

import puremagic


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


class Image:
    def __init__(self, data: bytes) -> None:
        self._data = data

        hash_maker = HashMaker("sha256")
        self._hashnized_name = hash_maker.make_from_binary(data)
        self._extension = puremagic.from_string(data)

    @property
    def hashnized_name(self) -> str:
        return self._hashnized_name

    def to_zipfile(self, zipf: zipfile.ZipFile) -> None:
        zipf.writestr(f"{self._hashnized_name}{self._extension}", self._data)


class DefaultBackgroudImage(Image):
    def __init__(self) -> None:
        pass

    @property
    def hashnized_name(self) -> str:
        return "testTableBackgroundImage_image"

    def to_zipfile(self, zipf: zipfile.ZipFile) -> None:
        pass
