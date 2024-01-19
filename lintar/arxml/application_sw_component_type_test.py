import unittest
from lxml import etree
from .application_sw_component_type import ApplicationSwComponentType


class ApplicationSwComponentTypeTests(unittest.TestCase):
    def setUp(self):
        # Create a sample XML element for testing
        xml_string = """
        <APPLICATION-SW-COMPONENT-TYPE  UUID="123">
            <SHORT-NAME>Component1</SHORT-NAME>
            <PORTS>
            </PORTS>
        </APPLICATION-SW-COMPONENT-TYPE>
        """
        self.xml_element = etree.fromstring(xml_string)

    def test_parse(self):
        # Call the parse method and check if the object is created correctly
        component = ApplicationSwComponentType.parse(self.xml_element)
        self.assertEqual(component.uuid, "123")
        self.assertEqual(component.short_name, "Component1")
        self.assertEqual(len(component.ports), 0)


if __name__ == "__main__":
    unittest.main()
