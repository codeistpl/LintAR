import argparse
import logging

from arxml.parser import ArxmlParser
from log_config import configure_logger
from validators.schema_based_validator import validate_arxml_with_schema

version = "0.1.0"


def parse_args():
    parser = argparse.ArgumentParser(
        description="LintAR the ARXML linting tool"
    )
    parser.add_argument(
        "file", metavar="FILE", type=str, help="Path to the input file"
    )
    parser.add_argument(
        "--log-level", default="INFO", help="Set the log level (default: INFO)"
    )
    parser.add_argument("--log-file", help="Path to the log file")

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {version}"
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    configure_logger(log_level=args.log_level, log_file=args.log_file)

    validate_arxml_with_schema(args.file)

    parser = ArxmlParser(args.file)
    app_sw_comp_types = parser.get_application_sw_component_types()
    for app_sw_comp_type in app_sw_comp_types:
        logging.info(app_sw_comp_type.short_name + " " + app_sw_comp_type.uuid)

        for port in app_sw_comp_type.ports:
            logging.info(port.short_name + " " + port.uuid)
            logging.info(port.interface_tref.text)


if __name__ == "__main__":
    main()
