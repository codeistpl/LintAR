import logging
from abc import ABC, abstractmethod

from lxml import etree as ET
from lxml.etree import Element


def catch_and_log_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logging.error(f"Exception occurred while parsing: {e}")
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
            raise ValueError(
                f"Missing required tag: {tag}, inside XML file line number {xmlElement.sourceline} \n{pretty_print(xmlElement)}"
            )

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

    def get_attrib_or_none(self, xmlElement: Element, attrib: str):
        return (
            xmlElement.attrib.get(attrib)
            if xmlElement.attrib.get(attrib) is not None
            else None
        )

    def get_attrib_or_rise(self, xmlElement: Element, attrib: str):
        attrib = self.get_attrib_or_none(xmlElement, attrib)
        if attrib is None:
            raise ValueError(
                f"Missing required attribute: {attrib}, inside XML file line number {xmlElement.sourceline} \n{pretty_print(xmlElement)}"
            )

        return attrib
