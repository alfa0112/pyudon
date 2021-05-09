from pathlib import Path
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from .util import HashMaker


def _add_card(node, front_hashed_name: str, back_hashed_name: str, x, y, size=2, state=0):
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
    front_image_data_node = ET.SubElement(base_image_data_node,
                                            "data",
                                            attrib={"type": "image",
                                                    "name": "front"})
    front_image_data_node.text = front_hashed_name
    back_image_data_node = ET.SubElement(base_image_data_node,
                                            "data",
                                            attrib={"type": "image",
                                                    "name": "back"})
    back_image_data_node.text = back_hashed_name

    common_data_node = ET.SubElement(data_card_node,
                            "data",
                            attrib={"name": "common"})
    name_data_node = ET.SubElement(common_data_node,
                            "data",
                            attrib={"name": "name"})
    name_data_node.text = "Card"
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

    def add_card_from_path(self, front_img_path: Path, back_img_path: Path, num=1, x=0, y=0, size=2, state=0):
        front_img_bin = front_img_path.open("rb").read()
        back_img_bin = back_img_path.open("rb").read()

        self.add_card_from_bin(front_img_bin, back_img_bin, num, x, y, size, state)

    def add_card_from_bin(self, front_img_bin: bytes, back_img_bin: bytes, num=1, x=0, y=0, size=2, state=0):
        front_hashed_name = self._hash_maker.make_from_binary(front_img_bin)
        back_hashed_name = self._hash_maker.make_from_binary(back_img_bin)

        for _ in range(num):
            _add_card(self._card_root_node, front_hashed_name, back_hashed_name, x, y, size, state)


class CharacterNode():
    def __init__(self, parent_node, name, size=1, x=0, y=0, z=0, img_identifier=""):
        self._parent_node = parent_node        
        self._resource_node = None

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

    def add_resource(self, name, max_value, current_value):
        if not self._resource_node:        
            self._resource_node = ET.SubElement(self._detail_node,
                                                "data",
                                                attrib={"name": "detail"})
        # <data type="numberResource" currentValue="200" name="HP">
        self._resource_node = ET.SubElement(self._resource_node,
                                            "data",
                                            attrib={"type": "numberResource",
                                                    "currentValue": str(current_value),
                                                    "name": name})
        self._resource_node.text = str(max_value)


class TableNode():
    def __init__(self,
                root_node,
                name,
                width=20,
                height=15,
                grid_size=50,
                image_identifier="testTableBackgroundImage_image",
                bg_image_identifier="imageIdentifier",
                bg_filter_type="",
                selected="true",
                grid_type=0,
                grid_color="#000000e6"):
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
    def __init__(self,
                root_node=None):
        self._hash_maker = HashMaker()

        if root_node:
            self._root_node = root_node
        else:
            self._root_node = ET.Element('room')            
            self._first_table_node = self.add_game_table("First table")        

    @property
    def first_table_node(self):
        return self._first_table_node

    def add_game_table(self,
                        name,
                        width=20,
                        height=15,
                        grid_size=50,
                        image_identifier="testTableBackgroundImage_image",
                        bg_image_identifier="imageIdentifier",
                        bg_filter_type="",
                        selected="true",
                        grid_type=0,
                        grid_color="#000000e6"):
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

    def add_character(self, name, size=1, x=0, y=0, z=0):
        return CharacterNode(self._root_node, name, size, x, y, z)

    def add_card_from_path(self, front_img_path: Path, back_img_path: Path, x=0, y=0, size=2, state=0):
        front_img_bin = front_img_path.open("rb").read()
        back_img_bin = back_img_path.open("rb").read()

        self.add_card_from_bin(front_img_bin, back_img_bin, x, y, size, state)        

    def add_card_from_bin(self, front_img_bin: bytes, back_img_bin: bytes, x=0, y=0, size=2, state=0):
        front_hashed_name = self._hash_maker.make_from_binary(front_img_bin)
        back_hashed_name = self._hash_maker.make_from_binary(back_img_bin)

        _add_card(self._root_node, front_hashed_name, back_hashed_name, x, y, size, state)
    
    def write(self, path, encoding="utf-8"):
        with path.open("w") as f:
            f.write(self.get_body())

    def get_body(self, encoding="utf-8") -> str:
        dom = md.parseString(ET.tostring(self._root_node, encoding))
        prettied = dom.toprettyxml(encoding=encoding)

        return prettied.decode(encoding)

