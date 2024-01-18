import unittest
from .ref import ProvidedInterfaceTref as Reference
from lxml import etree as ET


class TestReference(unittest.TestCase):
    def test_reference(self):
        xml = '<PROVIDED-INTERFACE-TREF DEST="destination">example</PROVIDED-INTERFACE-TREF>'
        element = ET.fromstring(xml)
        ref = Reference.parse(xmlElement=element)
        self.assertEqual(ref.text, "example")
        self.assertEqual(ref.dest, "destination")

    def test_getting_name(self):
        xml = '<PROVIDED-INTERFACE-TREF DEST="destination">/my/custom/reference/name</PROVIDED-INTERFACE-TREF>'
        element = ET.fromstring(xml)
        ref = Reference.parse(xmlElement=element)
        self.assertEqual(ref.name, "name")


if __name__ == "__main__":
    unittest.main()
