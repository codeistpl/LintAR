from dataclasses import dataclass, field
from typing import List
from .ports import Ports


@dataclass
class ApplicationSwComponentType:
    uuid = str = ""
    short_name: str = ""
    ports: Ports = field(default_factory=Ports)
    xmlElement = None

    @staticmethod
    def parse(xmlElement, namespace: str = ""):
        ns = namespace
        object = ApplicationSwComponentType()
        object.uuid = xmlElement.get("UUID")
        object.xmlElement = xmlElement
        object.short_name = xmlElement.find(f"{ns}SHORT-NAME").text
        object.ports = Ports.parse(xmlElement.find(f"{ns}PORTS"), ns)

        return object
