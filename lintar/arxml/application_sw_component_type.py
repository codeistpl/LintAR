import logging
from dataclasses import dataclass, field
from typing import List

from .abs_parser import (catch_and_log_exceptions, get_attrib_or_none,
                         get_element_or_none, get_text_or_rise, pretty_print)
from .ports import Ports


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
        object.uuid = get_attrib_or_none(xmlElement, ns, "UUID")
        if object.uuid is None:
            logging.warning(
                f"Missing UUID for APPLICATION-SW-COMPONENT-TYPE, inside XML file line number {xmlElement.sourceline} {pretty_print(xmlElement)}"
            )
            object.uuid = ""
        object.xmlElement = xmlElement
        object.short_name = get_text_or_rise(xmlElement, ns, "SHORT-NAME")
        object.ports = Ports.parse(
            get_element_or_none(xmlElement, ns, "PORTS"), ns
        )

        return object
