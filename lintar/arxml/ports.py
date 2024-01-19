from dataclasses import dataclass, field
from .ref import ProvidedInterfaceTref as Ref
from lxml.etree import Element
from abc import ABC, abstractmethod, abstractproperty
from typing import List
import logging
from .abs_parser import (
    catch_and_log_exceptions,
    get_text_or_rise,
    get_element_or_rise,
    get_attrib_or_none,
    pretty_print,
)


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
        ns = namespace
        arxml_ports = Ports()
        r_ports = xmlElement.findall(f"{ns}R-PORT-PROTOTYPE")
        for r_port in r_ports:
            arxml_ports.append(RPortPrototype.parse(r_port, ns))
        p_ports = xmlElement.findall(f"{ns}P-PORT-PROTOTYPE")
        for p_port in p_ports:
            arxml_ports.append(PPortPrototype.parse(p_port, ns))
        return arxml_ports

    @property
    def r_ports(self):
        return list(
            filter(lambda port: isinstance(port, RPortPrototype), self)
        )

    @property
    def p_ports(self):
        return list(
            filter(lambda port: isinstance(port, PPortPrototype), self)
        )
