from dataclasses import dataclass, field
from typing import List
from .ports import Ports
from .abs_parser import (
    get_text_or_rise,
    get_element_or_none,
    get_element_or_rise,
    catch_and_log_exceptions,
)


@dataclass
class ApplicationSwComponentType:
    uuid = str = ""
    short_name: str = ""
    ports: Ports = field(default_factory=Ports)
    xmlElement = None

    @staticmethod
    @catch_and_log_exceptions
    def parse(xmlElement, namespace: str = ""):
        ns = namespace
        object = ApplicationSwComponentType()
        object.uuid = xmlElement.get("UUID")
        object.xmlElement = xmlElement
        object.short_name = get_text_or_rise(xmlElement, ns, "SHORT-NAME")
        object.ports = Ports.parse(
            get_element_or_none(xmlElement, ns, "PORTS"), ns
        )

        return object
