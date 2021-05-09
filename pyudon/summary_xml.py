from pathlib import Path
import xml.dom.minidom as md
import xml.etree.ElementTree as ET


class SummaryXML():
    def __init__(self,
                root_node=None,
                data_tag="HP MP 敏捷度 生命力 精神力",
                sort_tag="name",
                sort_order="ASC"):
        if root_node:
            self._root_node = root_node
        else:
            self._root_node = ET.Element('summary-setting',
                                            attrib={"sortTag": sort_tag,
                                                    "sortOrder": sort_order,
                                                    "dataTag": data_tag})

    def write(self, path, encoding="utf-8"):
        with path.open("w") as f:
            f.write(self.get_body())

    def get_body(self, encoding="utf-8") -> str:
        dom = md.parseString(ET.tostring(self._root_node, encoding))
        prettied = dom.toprettyxml(encoding=encoding)

        return prettied.decode(encoding)

