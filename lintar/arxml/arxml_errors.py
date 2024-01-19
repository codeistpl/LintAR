class ArxmlParseError(Exception):
    def __init__(
        self, message: str = "ARXML parsing error", line_number: int = 0
    ):
        self.message = message
        self.line_number = line_number

    def __str__(self):
        return f"{self.message} at line {self.line_number}"


class MissingData(ArxmlParseError):
    pass
