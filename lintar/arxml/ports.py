import logging
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field
from typing import List

from lxml.etree import Element

from .abs_parser import (catch_and_log_exceptions, get_attrib_or_none,
                         get_element_or_rise, get_text_or_rise, pretty_print)
from .ref import ProvidedInterfaceTref as Ref


@dataclass
class AbsPortPrototype(ABC):
    @abstractproperty
    def interface_tref(self):
        pass

    @abstractmethod
    def parse(xmlElement, namespace: str = ""):
        pass


@dataclass
class PPortPrototype(AbsPortPrototype):
    provided_interface_tref: Ref = None

    @staticmethod
    @catch_and_log_exceptions
    def parse(xmlElement, namespace: str = ""):
        arxml_obj = PPortPrototype()
        ns: str = namespace
        arxml_obj.xmlElement = xmlElement
        arxml_obj.short_name = get_text_or_rise(xmlElement, ns, "SHORT-NAME")
        arxml_obj.provided_interface_tref = Ref.parse(
            get_element_or_rise(xmlElement, ns, "PROVIDED-INTERFACE-TREF"), ns
        )
        arxml_obj.uuid = get_attrib_or_none(xmlElement, ns, "UUID")
        if arxml_obj.uuid is None:
            logging.warning(
                f"Missing UUID for P-PORT-PROTOTYPE, inside XML file line number {xmlElement.sourceline} \n{pretty_print(xmlElement)}"
            )
            arxml_obj.uuid = ""
        return arxml_obj

    @property
    def interface_tref(self):
        return self.provided_interface_tref


@dataclass
class RPortPrototype(AbsPortPrototype):
    @staticmethod
    @catch_and_log_exceptions
    def parse(xmlElement, namespace: str = ""):
        ns = namespace
        arxml_obj = RPortPrototype()
        arxml_obj.xmlElement = xmlElement
        arxml_obj.short_name = get_text_or_rise(xmlElement, ns, "SHORT-NAME")
        arxml_obj.required_interface_tref = Ref.parse(
            get_element_or_rise(xmlElement, ns, "REQUIRED-INTERFACE-TREF"), ns
        )
        arxml_obj.uuid = get_attrib_or_none(xmlElement, ns, "UUID")
        return arxml_obj

    @property
    def interface_tref(self):
        return self.required_interface_tref


class Ports(List[AbsPortPrototype]):
    def parse(xmlElement, namespace: str = ""):
        if xmlElement is None:
            return Ports()

        ns = namespace
        arxml_ports = Ports()
        arxml_ports = [
            RPortPrototype.parse(r_port, ns)
            for r_port in xmlElement.findall(f"{ns}R-PORT-PROTOTYPE")
        ]
        arxml_ports.extend(
            [
                PPortPrototype.parse(p_port, ns)
                for p_port in xmlElement.findall(f"{ns}P-PORT-PROTOTYPE")
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
