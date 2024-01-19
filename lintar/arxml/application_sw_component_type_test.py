import unittest
from lxml import etree
from .application_sw_component_type import ApplicationSwComponentType


class ApplicationSwComponentTypeTests(unittest.TestCase):
    def test_parse_ok(self):
        xml_string = """
        <APPLICATION-SW-COMPONENT-TYPE  UUID="123">
            <SHORT-NAME>Component1</SHORT-NAME>
            <PORTS>
            </PORTS>
        </APPLICATION-SW-COMPONENT-TYPE>
        """
        xml_element = etree.fromstring(xml_string)

        # Call the parse method and check if the object is created correctly
        component = ApplicationSwComponentType.parse(xml_element)
        self.assertEqual(component.uuid, "123")
        self.assertEqual(component.short_name, "Component1")
        self.assertEqual(len(component.ports), 0)

    def test_parse_no_short_name(self):
        xml_string = """
        <APPLICATION-SW-COMPONENT-TYPE  UUID="123">
            <PORTS>
            </PORTS>
        </APPLICATION-SW-COMPONENT-TYPE>
        """
        xml_element = etree.fromstring(xml_string)

        # Call the parse method and check if the object is created correctly
        component = ApplicationSwComponentType.parse(xml_element)
        self.assertIsNone(component)

    def test_parse_no_ports(self):
        xml_string = """
        <APPLICATION-SW-COMPONENT-TYPE  UUID="123">
            <SHORT-NAME>Component1</SHORT-NAME>
        </APPLICATION-SW-COMPONENT-TYPE>
        """
        xml_element = etree.fromstring(xml_string)

        # Call the parse method and check if the object is created correctly
        component = ApplicationSwComponentType.parse(xml_element)
        self.assertEqual(0, len(component.ports))


if __name__ == "__main__":
    unittest.main()
