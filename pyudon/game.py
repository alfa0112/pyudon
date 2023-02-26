import zipfile
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path

from .chat_xml import ChatXML
from .data_xml import DataXML
from .summary_xml import SummaryXML
from .util import HashMaker, Image


class TableGridType(Enum):
    SQUARE = auto()
    HEX_VERTICAL = auto()
    HEX_HORIZONTAL = auto()


class TableGridColor(Enum):
    BLACK = auto()
    WHITE = auto()


class TableBackgroundFilter(Enum):
    NONE = auto()
    BLACK = auto()
    WHITE = auto()


@dataclass(frozen=True)
class Table:
    name: str
    image: Image
    width: float = 20
    height: float = 20
    background_image: Image = None
    grid_type: TableGridType = TableGridType.SQUARE
    grid_color: TableGridColor = TableGridColor.BLACK
    background_filter: TableBackgroundFilter = TableBackgroundFilter.NONE
    show_grid: bool = False


@dataclass(frozen=True)
class CharacterResource:
    name: str
    initial_value: float
    max_value: float


@dataclass(frozen=True)
class Character:
    name: str
    size: float = 1
    resources: list[CharacterResource] = field(default_factory=list)
    image: Image = None
    info: str = None


@dataclass(frozen=True)
class Card:
    name: str
    front_image: Image
    back_image: Image


class Deck:
    name: str
    card_list: list[Card]

    def add_card(self, card: Card) -> None:
        pass

    def add_cards(self, cards: list[Card]) -> None:
        pass


class DiceType(Enum):
    SIDED_4 = auto()
    SIDED_6 = auto()
    SIDED_8 = auto()
    SIDED_10 = auto()
    SIDED_10_PLACES_10 = auto()
    SIDED_12 = auto()
    SIDED_20 = auto()


@dataclass(frozen=True)
class Dice:
    name: str
    type: DiceType


class Game:
    def __init__(self, table: Table) -> None:
        self._data_xml = DataXML()
        self._chat_xml = ChatXML()
        self._summary_xml = SummaryXML()

        self._hash_maker = HashMaker()

        self._tables: list[Table] = [table]

    def create_zip(self, file_path: Path) -> None:
        # data.xml組み立て
        for table in self._tables:
            self._data_xml.add_game_table(
                table.name,
                table.width,
                table.height,
                image_identifier=table.image.hashnized_name
            )

        # ファイル書き込み
        with (file_path.open("bw") as f,
              zipfile.ZipFile(f, "w") as zipf):
            zipf.writestr("data.xml", self._data_xml.get_body())
            zipf.writestr("chat.xml", self._chat_xml.get_body())
            zipf.writestr("summary.xml", self._summary_xml.get_body())

            self._dump_all_images(zipf)

    def _dump_all_images(self, zipf: zipfile.ZipFile) -> None:
        for table in self._tables:
            table.image.to_zipfile(zipf)

    def add_table(self, table: Table) -> None:
        self._tables.append(table)

    def add_character(self, character: Character, x: float, y: float) -> None:
        pass

    def add_card(self, card: Card, x: float, y: float) -> None:
        pass

    def add_deck(self, deck: Deck, x: float, y: float) -> None:
        pass

    def add_dice(self, dice: Dice, x: float, y: float) -> None:
        pass

    def set_backgroud_image(self) -> None:
        pass
