import unittest
from .arxml_errors import ArxmlParseError


class TestArxmlParseError(unittest.TestCase):
    def test_error_str(self):
        error = ArxmlParseError()
        self.assertEqual(str(error), "ARXML parsing error at line 0")


if __name__ == "__main__":
    unittest.main()
