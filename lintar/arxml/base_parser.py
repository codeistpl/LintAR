import logging
from abc import ABC, abstractmethod

from lxml import etree as ET
from lxml.etree import Element
from .arxml_errors import MissingData, ArxmlParseError


def catch_and_log_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ArxmlParseError, MissingData) as e:
            logging.error(e)
            return None

    return wrapper


def pretty_print(element: Element):
    return (
        ET.tostring(element, pretty_print=True)
        .decode("utf-8")
        .replace("  ", "")
    )


class BaseParser:
    def __init__(self, namespace: str = "", arxml_path: str = "") -> None:
        self.namespace = namespace
        self.arxml_path = arxml_path
        pass

    def get_element_or_none(self, xmlElement: Element, tag: str):
        return (
            xmlElement.find(f"{self.namespace}{tag}")
            if xmlElement.find(f"{self.namespace}{tag}") is not None
            else None
        )

    def get_element_or_rise(self, xmlElement: Element, tag: str):
        element = self.get_element_or_none(xmlElement, tag)
        if element is None:
            file_ref = f"{self.arxml_path}:{xmlElement.sourceline}"
            raise MissingData(f"{file_ref} Missing required tag: {tag} !")

        return element

    def get_text_or_none(
        self,
        xmlElement: Element,
        tag: str,
        is_optional: bool = False,
    ):
        return self.get_element_or_none(xmlElement, tag, is_optional).text

    def get_text_or_rise(self, xmlElement: Element, tag: str):
        element = self.get_element_or_rise(xmlElement, tag)
        return element.text

    def _get_attrib_or_none(self, xmlElement: Element, attrib: str):
        attrib = (
            xmlElement.attrib.get(attrib)
            if xmlElement.attrib.get(attrib) is not None
            else None
        )
        return attrib

    def get_optional_attrib(self, xmlElement: Element, attrib: str):
        val = self._get_attrib_or_none(xmlElement, attrib)
        if val is None:
            file_ref = f"{self.arxml_path}:{xmlElement.sourceline}"
            logging.warning(
                f"{file_ref} Missing optional attribute: {attrib}!"
            )
            return ""
        return val

    def get_attrib_or_rise(self, xmlElement: Element, attrib: str):
        attrib = self._get_attrib_or_none(xmlElement, attrib)
        if attrib is None:
            file_ref = f"{self.arxml_path}:{xmlElement.sourceline}"
            raise MissingData(
                f"{file_ref} Missing required attribute: {attrib}!"
            )

        return attrib
