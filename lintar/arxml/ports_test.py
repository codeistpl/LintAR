from unittest import TestCase
from lxml import etree as ET
from .ports import PPortPrototype, RPortPrototype, Ports


class TestPPortPrototype(TestCase):
    def test_getting_name(self):
        xml = '<P-PORT-PROTOTYPE UUID="9dc49b58-a185-36d4-8594-1e564711dd28">\
                  <SHORT-NAME>Status</SHORT-NAME>\
                  <PROVIDED-INTERFACE-TREF DEST="SENDER-RECEIVER-INTERFACE">/Demo/Interfaces/DoorStatus</PROVIDED-INTERFACE-TREF>\
                </P-PORT-PROTOTYPE>'
        element = ET.fromstring(xml)
        port = PPortPrototype.parse(xmlElement=element)
        self.assertEqual(port.short_name, "Status")
        self.assertEqual(
            port.provided_interface_tref.dest, "SENDER-RECEIVER-INTERFACE"
        )
        self.assertEqual(
            port.provided_interface_tref.text, "/Demo/Interfaces/DoorStatus"
        )
        self.assertEqual(port.uuid, "9dc49b58-a185-36d4-8594-1e564711dd28")


class TestRPortPrototype(TestCase):
    def test_getting_name(self):
        xml = '<R-PORT-PROTOTYPE UUID="9dc49b58-a185-36d4-8594-1e564711dd28">\
                  <SHORT-NAME>Status</SHORT-NAME>\
                  <REQUIRED-INTERFACE-TREF DEST="SENDER-RECEIVER-INTERFACE">/Demo/Interfaces/DoorStatus</REQUIRED-INTERFACE-TREF>\
                </R-PORT-PROTOTYPE>'
        element = ET.fromstring(xml)
        port = RPortPrototype.parse(xmlElement=element)
        self.assertEqual(port.short_name, "Status")
        self.assertEqual(
            port.required_interface_tref.dest, "SENDER-RECEIVER-INTERFACE"
        )
        self.assertEqual(
            port.required_interface_tref.text, "/Demo/Interfaces/DoorStatus"
        )
        self.assertEqual(port.uuid, "9dc49b58-a185-36d4-8594-1e564711dd28")


class TestPorts(TestCase):
    def test_ports(self):
        xml = '<PORTS>\
                <R-PORT-PROTOTYPE UUID="3179e3a7-1b49-3950-86db-d5c615049fb4">\
                  <SHORT-NAME>StatusLeft</SHORT-NAME>\
                  <REQUIRED-INTERFACE-TREF DEST="SENDER-RECEIVER-INTERFACE">/Demo/Interfaces/DoorStatus</REQUIRED-INTERFACE-TREF>\
                </R-PORT-PROTOTYPE>\
                <R-PORT-PROTOTYPE UUID="6f3c8fac-0a52-381b-a69a-9387a3306235">\
                  <SHORT-NAME>StatusRight</SHORT-NAME>\
                  <REQUIRED-INTERFACE-TREF DEST="SENDER-RECEIVER-INTERFACE">/Demo/Interfaces/DoorStatus</REQUIRED-INTERFACE-TREF>\
                </R-PORT-PROTOTYPE>\
                <P-PORT-PROTOTYPE UUID="5a63577a-a4d8-342f-8daf-d7cf49be95b3">\
                  <SHORT-NAME>CombinedStatus</SHORT-NAME>\
                  <PROVIDED-INTERFACE-TREF DEST="SENDER-RECEIVER-INTERFACE">/Demo/Interfaces/CombinedStatus</PROVIDED-INTERFACE-TREF>\
                </P-PORT-PROTOTYPE>\
              </PORTS>'
        element = ET.fromstring(xml)
        ports = Ports.parse(xmlElement=element)
        self.assertEqual(len(ports), 3)
        self.assertEqual(ports[0].short_name, "StatusLeft")
        self.assertEqual(ports[1].short_name, "StatusRight")
        self.assertEqual(ports[2].short_name, "CombinedStatus")
        self.assertEqual(len(ports.r_ports), 2)
        self.assertEqual(len(ports.p_ports), 1)
