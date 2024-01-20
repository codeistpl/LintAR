import logging
from dataclasses import dataclass, field
from typing import List

from lxml.etree import Element

from .base_parser import BaseParser, catch_and_log_exceptions, pretty_print
from .ports import Ports


@dataclass
class ApplicationSwComponentType:
    uuid = str = ""
    short_name: str = ""
    ports: Ports = field(default_factory=Ports)
    xmlElement = None

    class Parser(BaseParser):
        def __init__(self, namespace: str = "", arxml_path: str = "") -> None:
            super().__init__(namespace, arxml_path)

        @catch_and_log_exceptions
        def parse(self, xmlElement: Element):
            object = ApplicationSwComponentType()
            object.uuid = self.get_attrib_or_none(xmlElement, "UUID")
            if object.uuid is None:
                logging.warning(
                    f"Missing UUID for APPLICATION-SW-COMPONENT-TYPE, inside XML file line number {xmlElement.sourceline} {pretty_print(xmlElement)}"
                )
                object.uuid = ""
            object.xmlElement = xmlElement
            object.short_name = self.get_text_or_rise(xmlElement, "SHORT-NAME")
            object.ports = Ports.Parser(namespace=self.namespace).parse(
                self.get_element_or_none(xmlElement, "PORTS")
            )

            return object
