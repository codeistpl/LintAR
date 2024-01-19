from dataclasses import dataclass, field
from .ref import ProvidedInterfaceTref as Ref
from lxml.etree import Element
from abc import ABC, abstractmethod, abstractproperty
from typing import List


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
    def parse(xmlElement, namespace: str = ""):
        arxml_obj = PPortPrototype()
        ns: str = namespace
        arxml_obj.xmlElement = xmlElement
        arxml_obj.short_name = xmlElement.find(f"{ns}SHORT-NAME").text
        arxml_obj.provided_interface_tref = Ref.parse(
            xmlElement.find(f"{ns}PROVIDED-INTERFACE-TREF"), ns
        )
        arxml_obj.uuid = xmlElement.get("UUID")
        return arxml_obj

    @property
    def interface_tref(self):
        return self.provided_interface_tref


@dataclass
class RPortPrototype(AbsPortPrototype):
    @staticmethod
    def parse(xmlElement, namespace: str = ""):
        ns = namespace
        arxml_obj = RPortPrototype()
        arxml_obj.xmlElement = xmlElement
        arxml_obj.short_name = xmlElement.find(f"{ns}SHORT-NAME").text
        arxml_obj.required_interface_tref = Ref.parse(
            xmlElement.find(f"{ns}REQUIRED-INTERFACE-TREF"), ns
        )
        arxml_obj.uuid = xmlElement.get("UUID")

        arxml_obj.required_interface_tref = Ref.parse(
            xmlElement.find(f"{ns}REQUIRED-INTERFACE-TREF"), ns
        )
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

        print(arxml_ports)
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
