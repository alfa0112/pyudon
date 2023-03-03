import xml.dom.minidom as md
import xml.etree.ElementTree as ET
from pathlib import Path

from .util import HashMaker


def _add_card(node: ET.Element, name: str, top_hashed_name: str, bottom_hashed_name: str, x, y, size=2, state=0):
    card_node = ET.SubElement(node,
                              "card",
                              attrib={"location.name": "table",
                                      "location.x": str(x),
                                      "location.y": str(y),
                                      "posZ": "0",
                                      "state": str(state),
                                      "rotate": "0",
                                      "zindex": "0",
                                      "owner": ""})
    data_card_node = ET.SubElement(card_node,
                                   "data",
                                   attrib={"name": "card"})
    base_image_data_node = ET.SubElement(data_card_node,
                                         "data",
                                         attrib={"name": "image"})
    ET.SubElement(base_image_data_node,
                  "data",
                  attrib={"type": "image",
                          "name": "imageIdentifier"})
    top_image_data_node = ET.SubElement(base_image_data_node,
                                          "data",
                                          attrib={"type": "image",
                                                  "name": "front"})
    top_image_data_node.text = top_hashed_name
    bottom_image_data_node = ET.SubElement(base_image_data_node,
                                         "data",
                                         attrib={"type": "image",
                                                 "name": "back"})
    bottom_image_data_node.text = bottom_hashed_name

    common_data_node = ET.SubElement(data_card_node,
                                     "data",
                                     attrib={"name": "common"})
    name_data_node = ET.SubElement(common_data_node,
                                   "data",
                                   attrib={"name": "name"})
    name_data_node.text = name
    size_data_node = ET.SubElement(common_data_node,
                                   "data",
                                   attrib={"name": "size"})
    size_data_node.text = str(size)

    ET.SubElement(data_card_node,
                  "data",
                  attrib={"name": "detail"})


class DeckNode():
    def __init__(self, deck_node, card_root_node):
        self._deck_node = deck_node
        self._card_root_node = card_root_node

        self._hash_maker = HashMaker()

    def add_card(self, name: str, top_hashed_name: str, bottom_hashed_name: str,
                 num=1, x=0, y=0, size=2, state=0):
        for _ in range(num):
            _add_card(self._card_root_node, name, top_hashed_name,
                      bottom_hashed_name, x, y, size, state)


class CharacterDetailSectionNode:
    def __init__(self, parent_node: ET.Element, title: str):
        self._node = ET.SubElement(
            parent_node,
            "data",
            attrib=dict(
                name=title
            )
        )

    def add_resource(self, name: str, current_value: float, max_value: float) -> None:
        self._resource_node = ET.SubElement(
            self._node,
            "data",
            attrib={"type": "numberResource",
                    "currentValue": str(current_value),
                    "name": name}
        )
        self._resource_node.text = str(max_value)

    def add_note(self, title: str, value: str) -> None:
        # <data type="note" name="Desctiprion">
        self._item_node = ET.SubElement(
            self._node,
            "data",
            attrib=dict(
                type="note",
                name=title
            )
        )
        self._item_node.text = value


class CharacterNode():
    def __init__(self, parent_node, name, size=1, x=0, y=0, z=0, img_identifier=""):
        self._parent_node = parent_node
        self._resource_node = None
        self._info_node = None

        # <character>
        char_node = ET.SubElement(self._parent_node,
                                  "character",
                                  attrib={"location.name": "table",
                                          "location.x": str(x),
                                          "location.y": str(y),
                                          "posZ": str(z),
                                          "rotate": "0",
                                          "roll": "0"})
        #   <data name="character">
        char_data_char_node = ET.SubElement(char_node,
                                            "data",
                                            attrib={"name": "character"})
        #       <data name="image">
        char_data_image_node = ET.SubElement(char_data_char_node,
                                             "data",
                                             attrib={"name": "image"})
        #           <data type="image" name="imageIdentifier">
        char_data_image_identifier_node = ET.SubElement(char_data_image_node,
                                                        "data",
                                                        attrib={"type": "image",
                                                                "name": "imageIdentifier"})
        char_data_image_identifier_node.text = img_identifier

        #       <data name="common">
        char_data_common_node = ET.SubElement(char_data_char_node,
                                              "data",
                                              attrib={"name": "common"})
        #           <data name="name">
        char_data_common_name_node = ET.SubElement(char_data_common_node,
                                                   "data",
                                                   attrib={"name": "name"})
        char_data_common_name_node.text = name
        #           <data name="size">
        char_data_common_size_node = ET.SubElement(char_data_common_node,
                                                   "data",
                                                   attrib={"name": "size"})
        char_data_common_size_node.text = str(size)
        #       <data name="detail">
        self._detail_node = ET.SubElement(char_data_char_node,
                                          "data",
                                          attrib={"name": "detail"})

    def add_detail_section(self, title: str) -> CharacterDetailSectionNode:
        """_summary_

        Args:
            title (str): _description_

        Returns:
            _type_: _description_
        """
        return CharacterDetailSectionNode(
            self._detail_node,
            title
        )


class TableNode():
    def __init__(self,
                 root_node: ET.Element,
                 name: str,
                 width: float=20,
                 height: float=15,
                 grid_size: float=50,
                 image_identifier: str="testTableBackgroundImage_image",
                 bg_image_identifier: str="imageIdentifier",
                 bg_filter_type: str="",
                 selected: str="true",
                 grid_type: int=0,
                 grid_color: str="#000000e6"):
        self._hash_maker = HashMaker()
        self._table_node = ET.SubElement(root_node,
                                         'game-table',
                                         attrib={"name": name,
                                                 "width": str(width),
                                                 "height": str(height),
                                                 "gridSize": str(grid_size),
                                                 "imageIdentifier": image_identifier,
                                                 "backgroundImageIdentifier": bg_image_identifier,
                                                 "backgroundFilterType": bg_filter_type,
                                                 "selected": selected,
                                                 "gridType": str(grid_type),
                                                 "gridColor": grid_color})

    def set_width(self, width):
        self._table_node.set("width", str(width))

    def set_height(self, height):
        self._table_node.set("height", str(height))

    def set_img_from_path(self, img_path):
        hashed_img_name = self._hash_maker.make_from_file(img_path)
        self._table_node.set("imageIdentifier", hashed_img_name)

    def set_bg_img_from_path(self, img_path):
        hashed_img_name = self._hash_maker.make_from_file(img_path)
        self._table_node.set("backgroundImageIdentifier", hashed_img_name)


class DataXML():
    def __init__(self):
        self._hash_maker = HashMaker()

        self._root_node = ET.Element('room')

    def add_game_table(self,
                       name: str,
                       width: float=20,
                       height: float=15,
                       grid_size: float=50,
                       image_identifier: str="testTableBackgroundImage_image",
                       bg_image_identifier: str="imageIdentifier",
                       bg_filter_type: str="",
                       selected: str="true",
                       grid_type: int=0,
                       grid_color: str="#000000e6"):
        return TableNode(self._root_node,
                         name,
                         width=width,
                         height=height,
                         grid_size=grid_size,
                         image_identifier=image_identifier,
                         bg_image_identifier=bg_image_identifier,
                         bg_filter_type=bg_filter_type,
                         selected=selected,
                         grid_type=grid_type,
                         grid_color=grid_color)

    def add_card_stack(self, name, x=0, y=0, z=0) -> DeckNode:
        card_stack_node = ET.SubElement(self._root_node,
                                        "card-stack",
                                        attrib={"location.name": "table",
                                                "location.x": str(x),
                                                "location.y": str(y),
                                                "posZ": str(z),
                                                "rotate": "0",
                                                "zindex": "0",
                                                "owner": "",
                                                "isShowTotal": "true"})
        base_data_node = ET.SubElement(card_stack_node,
                                       "data",
                                       attrib={"name": "card-stack"})
        type_data_node = ET.SubElement(base_data_node,
                                       "data",
                                       attrib={"name": "image"})
        ET.SubElement(type_data_node,
                      "data",
                      attrib={"type": "image",
                              "name": "imageIdentifier"})

        common_data_node = ET.SubElement(base_data_node,
                                         "data",
                                         attrib={"name": "common"})
        name_data_node = ET.SubElement(common_data_node,
                                       "data",
                                       attrib={"name": "name"})
        name_data_node.text = name
        ET.SubElement(base_data_node,
                      "data",
                      attrib={"name": "detail"})

        card_root_node = ET.SubElement(card_stack_node,
                                       "node",
                                       attrib={"name": "cardRoot"})

        return DeckNode(card_stack_node, card_root_node)

    def add_character(self, name: str, size: float = 1, x: float = 0, y: float = 0, z: float = 0,
                      img_identifier: str = "") -> CharacterNode:
        return CharacterNode(self._root_node, name, size, x, y, z, img_identifier)

    def add_card(self, name: str, top_hashed_name: str, bottom_hashed_name: str,
                 x: float = 0, y: float = 0, size: float = 2, state: float = 0) -> None:
        _add_card(self._root_node, name, top_hashed_name,
                  bottom_hashed_name, x, y, size, state)

    def write(self, path, encoding="utf-8"):
        with path.open("w") as f:
            f.write(self.get_body())

    def get_body(self, encoding: str = "utf-8") -> str:
        # 最小構成のDOMを作成
        dom = md.parseString(ET.tostring(self._root_node, encoding))

        # 成形済みxml文字列を返す
        return dom.toprettyxml()
