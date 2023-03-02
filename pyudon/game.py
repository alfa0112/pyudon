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
    curret_value: float
    max_value: float


@dataclass(frozen=True)
class CharacterNote:
    name: str
    value: str


@dataclass
class CharacterDetailSection:
    name: str
    notes: list[CharacterNote] = field(default_factory=list)
    resources: list[CharacterResource] = field(default_factory=list)

    def add_note(self, item: CharacterNote):
        self.notes.append(item)

    def add_resource(self, item: CharacterResource):
        self.resources.append(item)


@dataclass
class Character:
    name: str
    size: float = 1
    image: Image = None
    detail_sections: list[CharacterDetailSection] = field(default_factory=list)

    def add_detail_section(self, detail_section: CharacterDetailSection) -> None:
        self.detail_sections.append(detail_section)


@dataclass(frozen=True)
class OnBoardCharacter:
    character: Character
    x: float
    y: float


class CardState(Enum):
    TOP = 0
    BOTTOM = 1


@dataclass(frozen=True)
class Card:
    name: str
    top_image: Image
    bottom_image: Image
    size: float = 2.0
    state: CardState = CardState.TOP


@dataclass(frozen=True)
class OnBoardCard:
    card: Card
    x: float
    y: float


@dataclass
class Deck:
    name: str
    cards: list[Card] = field(default_factory=list)

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def add_cards(self, cards: list[Card]) -> None:
        self.cards.extend(cards)


@dataclass
class OnBoardDeck:
    deck: Deck
    x: float
    y: float


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
        self._on_board_characters: list[OnBoardCharacter] = []
        self._on_board_cards: list[OnBoardCard] = []
        self._on_board_decks: list[OnBoardDeck] = []

    def create_zip(self, file_path: Path) -> None:
        # data.xml組み立て
        for table in self._tables:
            self._data_xml.add_game_table(
                table.name,
                table.width,
                table.height,
                image_identifier=table.image.hashnized_name
            )
        for on_board_character in self._on_board_characters:
            character = on_board_character.character
            if character.image:
                img_identifier = character.image.hashnized_name
            else:
                img_identifier = None
            character_node = self._data_xml.add_character(
                character.name,
                character.size,
                x=on_board_character.x,
                y=on_board_character.y,
                img_identifier=img_identifier
            )
            for detail_section in character.detail_sections:
                detail_section_node = character_node.add_detail_section(detail_section.name)
                for resource in detail_section.resources:
                    detail_section_node.add_resource(
                        resource.name,
                        resource.curret_value,
                        resource.max_value
                    )
                for note in detail_section.notes:
                    detail_section_node.add_note(
                        note.name,
                        note.value
                    )
        for on_board_card in self._on_board_cards:
            self._data_xml.add_card(
                on_board_card.card.name,
                on_board_card.card.top_image.hashnized_name,
                on_board_card.card.bottom_image.hashnized_name,
                on_board_card.x,
                on_board_card.y,
                on_board_card.card.size,
                on_board_card.card.state.value
            )
        for on_board_deck in self._on_board_decks:
            deck_node = self._data_xml.add_card_stack(
                on_board_deck.deck.name,
                on_board_deck.x,
                on_board_deck.y
            )
            for card in on_board_deck.deck.cards:
                deck_node.add_card(
                    card.name,
                    card.top_image.hashnized_name,
                    card.bottom_image.hashnized_name
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
        for on_board_character in self._on_board_characters:
            if on_board_character.character.image:
                on_board_character.character.image.to_zipfile(zipf)
        for on_board_card in self._on_board_cards:
            on_board_card.card.top_image.to_zipfile(zipf)
            on_board_card.card.bottom_image.to_zipfile(zipf)

    def add_table(self, table: Table) -> None:
        self._tables.append(table)

    def add_character(self, character: Character, x: float, y: float) -> None:
        self._on_board_characters.append(OnBoardCharacter(character, x, y))

    def add_card(self, card: Card, x: float, y: float) -> None:
        self._on_board_cards.append(OnBoardCard(card, x, y))

    def add_deck(self, deck: Deck, x: float, y: float) -> None:
        self._on_board_decks.append(OnBoardDeck(deck, x, y))

    def add_dice(self, dice: Dice, x: float, y: float) -> None:
        pass

    def set_backgroud_image(self) -> None:
        pass
