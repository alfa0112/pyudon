import xml.dom.minidom as md
import xml.etree.ElementTree as ET
from pathlib import Path


class ChatXML():
    def __init__(self, root_node: ET.Element = None) -> None:
        if root_node:
            self._root_node = root_node
        else:
            self._root_node = ET.Element('chat-tab-list')
            self.add_chat_tab("MainTab")
            self.add_chat_tab("SubTab")

    def add_chat_tab(self, name: str) -> None:
        ET.SubElement(self._root_node,
                      "chat-tab",
                      attrib={"name": name})

    def write(self, path: Path, encoding: str = "utf-8") -> None:
        with path.open("w") as f:
            f.write(self.get_body(encoding))

    def get_body(self, encoding: str = "utf-8") -> str:
        # 最小構成のDOMを作成
        dom = md.parseString(ET.tostring(self._root_node, encoding))

        # 成形済みxml文字列を返す
        return dom.toprettyxml()
