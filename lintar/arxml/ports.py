import logging
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field
from typing import List

from lxml.etree import Element

from .base_parser import BaseParser, catch_and_log_exceptions, pretty_print
from .ref import ProvidedInterfaceTref as Ref


@dataclass
class AbsPortPrototype(ABC):
    @abstractproperty
    def interface_tref(self):
        pass


@dataclass
class PPortPrototype(AbsPortPrototype):
    provided_interface_tref: Ref = None

    class Parser(BaseParser):
        def __init__(self, namespace: str = "", arxml_path: str = "") -> None:
            super().__init__(namespace, arxml_path)

        @catch_and_log_exceptions
        def parse(self, xmlElement):
            port = PPortPrototype()
            port.xmlElement = xmlElement
            port.short_name = self.get_text_or_rise(xmlElement, "SHORT-NAME")
            port.provided_interface_tref = Ref.parse(
                self.get_element_or_rise(
                    xmlElement, "PROVIDED-INTERFACE-TREF"
                ),
            )
            port.uuid = self.get_optional_attrib(xmlElement, "UUID")
            return port

    @property
    def interface_tref(self):
        return self.provided_interface_tref


@dataclass
class RPortPrototype(AbsPortPrototype):
    class Parser(BaseParser):
        def __init__(self, namespace: str = "", arxml_path: str = "") -> None:
            super().__init__(namespace, arxml_path)

        @catch_and_log_exceptions
        def parse(self, xmlElement):
            port = RPortPrototype()
            port.xmlElement = xmlElement
            port.short_name = self.get_text_or_rise(xmlElement, "SHORT-NAME")
            port.required_interface_tref = Ref.parse(
                self.get_element_or_rise(
                    xmlElement, "REQUIRED-INTERFACE-TREF"
                ),
            )
            port.uuid = self.get_optional_attrib(xmlElement, "UUID")
            return port

    @property
    def interface_tref(self):
        return self.required_interface_tref


class Ports(List[AbsPortPrototype]):
    class Parser(BaseParser):
        def parse(self, xmlElement: Element):
            if xmlElement is None:
                return Ports()

            arxml_ports = Ports()
            arxml_ports = [
                RPortPrototype.Parser(self.namespace, self.arxml_path).parse(
                    r_port
                )
                for r_port in xmlElement.findall(
                    f"{self.namespace}R-PORT-PROTOTYPE"
                )
            ]
            arxml_ports.extend(
                [
                    PPortPrototype.Parser(
                        self.namespace, self.arxml_path
                    ).parse(p_port)
                    for p_port in xmlElement.findall(
                        f"{self.namespace}P-PORT-PROTOTYPE"
                    )
                ]
            )
            return Ports(filter(lambda port: port is not None, arxml_ports))

    @property
    def r_ports(self):
        return Ports(
            filter(lambda port: isinstance(port, RPortPrototype), self)
        )

    @property
    def p_ports(self):
        return Ports(
            filter(lambda port: isinstance(port, PPortPrototype), self)
        )
