import zipfile

import puremagic

from .util import HashMaker


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
