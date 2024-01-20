from lxml import etree as ET

from .application_sw_component_type import ApplicationSwComponentType


class ArxmlParser:
    def __init__(self, arxml_path):
        self.arxml_path = arxml_path
        self.tree = ET.parse(arxml_path)
        self.root = self.tree.getroot()
        self.ns = self.root.tag.split("}")[0] + "}"

    def get_application_sw_component_types(self):
        objects = []
        xmlElements = self.root.findall(
            f".//{self.ns}APPLICATION-SW-COMPONENT-TYPE"
        )

        for element in xmlElements:
            objects.append(
                ApplicationSwComponentType.parse(
                    xmlElement=element, namespace=self.ns
                )
            )

        return objects
