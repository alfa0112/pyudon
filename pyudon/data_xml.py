import hashlib
from pathlib import Path
import xml.etree.ElementTree as ET

from .util import FileToHashMaker


class DeckNode():
    def __init__(self, deck_node, card_root_node):
        self._deck_node = deck_node
        self._card_root_node = card_root_node

    def add_card(self, front_img: str, back_img: str, size=2):
        card_node = ET.SubElement(self._card_root_node,
                                "card",
                                attrib={"location.name": "table",
                                        "location.x": "0",
                                        "location.y": "0",
                                        "posZ": "0",
                                        "state": "1",
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
        front_image_data_node.text = Path(front_img).stem
        back_image_data_node = ET.SubElement(base_image_data_node,
                                                "data",
                                                attrib={"type": "image",
                                                        "name": "back"})
        back_image_data_node.text = Path(back_img).stem

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


class RoomNode():
    def __init__(self, root_node):
        self._root_node = root_node

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

    def add_card(self, front_img: str, back_img: str, x, y, size=2, state=0):
        card_node = ET.SubElement(self._root_node,
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
        front_image_data_node.text = Path(front_img).stem
        back_image_data_node = ET.SubElement(base_image_data_node,
                                                "data",
                                                attrib={"type": "image",
                                                        "name": "back"})
        back_image_data_node.text = Path(back_img).stem

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




