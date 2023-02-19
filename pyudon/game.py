import random
import zipfile
from pathlib import Path

from pandas import DataFrame

from .chat_xml import ChatXML
from .data_xml import DataXML
from .summary_xml import SummaryXML
from .util import HashMaker


class Game:
    def __init__(self):
        self._data_xml = DataXML()
        self._chat_xml = ChatXML()
        self._summary_xml = SummaryXML()

        self._hash_maker = HashMaker()

    def create_zip(self, file_path: Path):
        with (file_path.open("bw") as f,
              zipfile.ZipFile(f, "w") as zipf):
            zipf.writestr("data.xml", self._data_xml.get_body())
            zipf.writestr("chat.xml", self._chat_xml.get_body())
            zipf.writestr("summary.xml", self._summary_xml.get_body())


class Deck:
    pass


class CardImageTable():
    def __init__(self, img_dir: Path, card_image_table_df: DataFrame):
        self._card_image_table_df = card_image_table_df.copy()
        self._card_image_table_df["image"] = self._card_image_table_df["image"].map(lambda name: img_dir / name)

        self._dict = {series["name"]: series["image"]
                        for _, series
                        in self._card_image_table_df.iterrows()}

    def get_dict(self) -> dict:
        return self._dict

    def iter_img_paths(self):
        for _, series in self._card_image_table_df.iterrows():
            yield series["image"]


class Card():
    def __init__(self, name, front, back):
        self._name = name
        self._front = front
        self._back = back

    @property
    def name(self):
        return self._name

    @property
    def front(self):
        return self._front

    @property
    def back(self):
        return self._back


class ClockWorkerDataXML():
    def __init__(self,
                cards_image_dict,
                table_image_path=None):
        self._data_xml = DataXML()
        self._data_xml.first_table_node.set_height(0)
        self._data_xml.first_table_node.set_width(0)
        if table_image_path:
            self._data_xml.first_table_node.set_bg_img_from_path(table_image_path)

        player_1 = self._data_xml.add_character("Player1", size=2, x=-450, y=-200)
        player_1.add_resource("VP", 100, 0)

        self._cards_image_dict = cards_image_dict

        self._magical_sercle_deck_lv1_red = self._data_xml.add_card_stack("MagicalSercleCardDeckLv1Red",
                                                                -300, -200)
        self._magical_sercle_deck_lv1_red.add_card_from_path(self._cards_image_dict["sercle1red"],
                                                            self._cards_image_dict["back"],
                                                            5)
        self._magical_sercle_deck_lv2_red = self._data_xml.add_card_stack("MagicalSercleCardDeckLv2Red",
                                                                -200, -200)
        self._magical_sercle_deck_lv2_red.add_card_from_path(self._cards_image_dict["sercle2red"],
                                                            self._cards_image_dict["back"],
                                                            5)
        self._magical_sercle_deck_lv3_red = self._data_xml.add_card_stack("MagicalSercleCardDeckLv2Red",
                                                                -100, -200)
        self._magical_sercle_deck_lv3_red.add_card_from_path(self._cards_image_dict["sercle3red"],
                                                            self._cards_image_dict["back"],
                                                            3)

        self._magical_sercle_deck_lv1_blue = self._data_xml.add_card_stack("MagicalSercleCardDeckLv1Blue",
                                                                -300, -50)
        self._magical_sercle_deck_lv1_blue.add_card_from_path(self._cards_image_dict["sercle1blue"],
                                                            self._cards_image_dict["back"],
                                                            5)
        self._magical_sercle_deck_lv2_blue = self._data_xml.add_card_stack("MagicalSercleCardDeckLv2Blue",
                                                                -200, -50)
        self._magical_sercle_deck_lv2_blue.add_card_from_path(self._cards_image_dict["sercle2blue"],
                                                            self._cards_image_dict["back"],
                                                            5)
        self._magical_sercle_deck_lv3_blue = self._data_xml.add_card_stack("MagicalSercleCardDeckLv3Blue",
                                                                -100, -50)
        self._magical_sercle_deck_lv3_blue.add_card_from_path(self._cards_image_dict["sercle3blue"],
                                                            self._cards_image_dict["back"],
                                                            3)

    def add_card_to_board(self, front_path, back_path, x, y, state=0):
        self._data_xml.add_card_from_path(front_path, back_path, x, y, state=state)

    def create_random_field(self, x=0, y=0, x_distance=100, y_distance=130):
        cards = []
        cards.extend([ClockWorkerCard("rock",
                                    self._cards_image_dict["rock"],
                                    self._cards_image_dict["back"])] * 2)
        cards.extend([ClockWorkerCard("1st",
                                    self._cards_image_dict["1st"],
                                    self._cards_image_dict["2pt"])] * 3)
        cards.extend([ClockWorkerCard("2nd",
                                    self._cards_image_dict["2nd"],
                                    self._cards_image_dict["1pt"])] * 10)
        cards.extend([ClockWorkerCard("3rd",
                                    self._cards_image_dict["3rd"],
                                    self._cards_image_dict["2pt"])] * 21)

        random.shuffle(cards)

        x = 0
        y = 0
        for card in cards:
            if x > x_distance * 5:
                x = 0
                y += y_distance
            self.add_card_to_board(card.front,
                                    card.back,
                                    x,
                                    y,
                                    state=0)
            x += x_distance

    def write(self, path, encoding="utf-8"):
        self._data_xml.write(path, encoding)

    def get_body(self, encoding="utf-8") -> str:
        return self._data_xml.get_body(encoding)
