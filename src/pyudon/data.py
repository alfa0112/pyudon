import zipfile
from abc import ABC, abstractmethod

import puremagic

from .util import HashMaker


class IImage(ABC):
    @abstractmethod
    def __eq__(self, __o: object) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @property
    @abstractmethod
    def hashnized_name(self) -> str:
        pass

    @abstractmethod
    def to_zipfile(self, zipf: zipfile.ZipFile) -> None:
        pass


class Image(IImage):
    def __init__(self, data: bytes) -> None:
        self._data = data

        hash_maker = HashMaker("sha256")
        self._hashnized_name = hash_maker.make_from_binary(data)
        self._extension = puremagic.from_string(data)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Image):
            return False
        return self._hashnized_name == __o._hashnized_name

    def __hash__(self) -> int:
        return int.from_bytes(self._hashnized_name.encode())

    @property
    def hashnized_name(self) -> str:
        return self._hashnized_name

    def to_zipfile(self, zipf: zipfile.ZipFile) -> None:
        zipf.writestr(f"{self._hashnized_name}{self._extension}", self._data)


class DefaultBackgroudImage(IImage):
    def __init__(self) -> None:
        pass

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, DefaultBackgroudImage)

    def __hash__(self) -> int:
        return int.from_bytes("DefaultBackgroudImage".encode())

    @property
    def hashnized_name(self) -> str:
        return "testTableBackgroundImage_image"

    def to_zipfile(self, zipf: zipfile.ZipFile) -> None:
        pass
