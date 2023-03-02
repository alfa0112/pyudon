import xml.dom.minidom as md
import xml.etree.ElementTree as ET
from pathlib import Path


class SummaryXML():
    def __init__(self,
                 root_node: ET.Element = None,
                 data_tag: str = "HP MP 敏捷度 生命力 精神力",
                 sort_tag: str = "name",
                 sort_order: str = "ASC") -> None:
        if root_node:
            self._root_node = root_node
        else:
            self._root_node = ET.Element('summary-setting',
                                         attrib={"sortTag": sort_tag,
                                                 "sortOrder": sort_order,
                                                 "dataTag": data_tag})

    def write(self, path: Path, encoding="utf-8") -> None:
        with path.open("w") as f:
            f.write(self.get_body(encoding))

    def get_body(self, encoding: str = "utf-8") -> str:
        # 最小構成のDOMを作成
        dom = md.parseString(ET.tostring(self._root_node, encoding))

        # 成形済みxml文字列を返す
        return dom.toprettyxml()
