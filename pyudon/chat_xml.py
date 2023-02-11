import xml.dom.minidom as md
import xml.etree.ElementTree as ET


class ChatXML():
    def __init__(self, root_node=None):
        if root_node:
            self._root_node = root_node
        else:
            self._root_node = ET.Element('chat-tab-list')
            self.add_chat_tab("Main Tab")
            self.add_chat_tab("Sub Tab")

    def add_chat_tab(self, name):
        ET.SubElement(self._root_node,
                      "chat-tab",
                      attrib={"name": name})

    def write(self, path, encoding="utf-8"):
        with path.open("w") as f:
            f.write(self.get_body())

    def get_body(self, encoding="utf-8") -> str:
        dom = md.parseString(ET.tostring(self._root_node, encoding))
        prettied = dom.toprettyxml(encoding=encoding)

        return prettied.decode(encoding)
