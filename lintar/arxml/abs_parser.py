import logging
from abc import ABC, abstractmethod

from lxml import etree as ET
from lxml.etree import Element


def catch_and_log_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Exception occurred while parsing: {e}")
            return None

    return wrapper


def pretty_print(element: Element):
    return (
        ET.tostring(element, pretty_print=True)
        .decode("utf-8")
        .replace("  ", "")
    )


def get_element_or_none(xmlElement: Element, namespace: str, tag: str):
    return (
        xmlElement.find(f"{namespace}{tag}")
        if xmlElement.find(f"{namespace}{tag}") is not None
        else None
    )


def get_element_or_rise(xmlElement: Element, namespace: str, tag: str):
    element = get_element_or_none(xmlElement, namespace, tag)
    if element is None:
        raise ValueError(
            f"Missing required tag: {tag}, inside XML file line number {xmlElement.sourceline} \n{pretty_print(xmlElement)}"
        )

    return element


def get_text_or_none(
    xmlElement: Element, namespace: str, tag: str, is_optional: bool = False
):
    return get_element_or_none(xmlElement, namespace, tag, is_optional).text


def get_text_or_rise(xmlElement: Element, namespace: str, tag: str):
    element = get_element_or_rise(xmlElement, namespace, tag)
    return element.text


def get_attrib_or_none(xmlElement: Element, namespace: str, attrib: str):
    return (
        xmlElement.attrib.get(attrib)
        if xmlElement.attrib.get(attrib) is not None
        else None
    )


def get_attrib_or_rise(xmlElement: Element, namespace: str, attrib: str):
    attrib = get_attrib_or_none(xmlElement, namespace, attrib)
    if attrib is None:
        raise ValueError(
            f"Missing required attribute: {attrib}, inside XML file line number {xmlElement.sourceline} \n{pretty_print(xmlElement)}"
        )

    return attrib


class AbsParser(ABC):
    @abstractmethod
    @catch_and_log_exceptions
    def parse(self, xmlElement: Element, namespace: str):
        pass


@catch_and_log_exceptions
def parse_xml(xmlElement: Element, namespace: str):
    # Your parsing logic here
    pass
