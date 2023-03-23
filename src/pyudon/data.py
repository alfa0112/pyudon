import zipfile
from abc import ABC, abstractmethod

import puremagic

from .util import HashMaker


class IImage(ABC):
    @property
    @abstractmethod
    def hashnized_name(self) -> str:
        pass

    @abstractmethod
    def to_zipfile(self, zipf: zipfile.ZipFile) -> None:
        pass

    @abstractmethod
    def __hash__(self) -> str:
        pass


class Image(IImage):
    def __init__(self, data: bytes) -> None:
        self._data = data

        hash_maker = HashMaker("sha256")
        self._hashnized_name = hash_maker.make_from_binary(data)
        self._extension = puremagic.from_string(data)

    def __hash__(self) -> str:
        return self._hashnized_name

    @property
    def hashnized_name(self) -> str:
        return self._hashnized_name

    def to_zipfile(self, zipf: zipfile.ZipFile) -> None:
        zipf.writestr(f"{self._hashnized_name}{self._extension}", self._data)


class DefaultBackgroudImage(IImage):
    def __init__(self) -> None:
        pass

    def __hash__(self) -> str:
        return "DefaultBackgroudImage"

    @property
    def hashnized_name(self) -> str:
        return "testTableBackgroundImage_image"

    def to_zipfile(self, zipf: zipfile.ZipFile) -> None:
        pass
