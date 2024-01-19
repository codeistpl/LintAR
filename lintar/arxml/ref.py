from dataclasses import dataclass


@dataclass
class Reference:
    text: str = None
    dest: str = None

    @staticmethod
    def parse(xmlElement, namespace: str = ""):
        ns = namespace
        data = Reference()
        data.text = xmlElement.text
        data.dest = xmlElement.get("DEST")
        return data

    @property
    def name(self):
        if not self.text:
            return ""
        return self.text.split("/")[-1]


@dataclass
class ProvidedInterfaceTref(Reference):
    pass
