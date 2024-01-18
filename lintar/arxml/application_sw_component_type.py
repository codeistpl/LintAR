from dataclasses import dataclass, field
from typing import List
from ports import Ports


@dataclass
class ApplicationSwComponentType:
    short_name: str = None
    ports: List[str] = field(default_factory=list)
    xmlElement = None

    @staticmethod
    def parse(xmlElement, namespace: str = None):
        ns = namespace
        data = ApplicationSwComponentType()
        data.xmlElement = xmlElement
        data.short_name = xmlElement.find(f"{ns}SHORT-NAME").text
        ports = Ports.parse(xmlElement.findall("PORTS"))
