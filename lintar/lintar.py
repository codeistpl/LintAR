import argparse
import logging

import colorlog
from arxml.parser import ArxmlParser
from validators.schema_based_validator import validate_arxml_with_schema
import os
import os


def configure_logger(log_file=None, log_level=logging.INFO):
    """
    Configure the logger with a console handler and an optional file handler.

    Args:
        log_file (str, optional): Path to the log file. Defaults to None.
        log_level (int, optional): Logging level. Defaults to logging.INFO.
    """

    # Check if the logger already has handlers
    if logging.getLogger().hasHandlers():
        return

    logger = logging.getLogger()

    # Check if log_file is provided
    if log_file:
        # Create a file handler and set the formatter
        file_handler = logging.FileHandler(log_file)
        fmt = (
            "%(asctime)s| %(levelname)-8s| %(filename)s:%(lineno)d | %(message)s"
            if log_level == logging.DEBUG
            else "%(asctime)s| %(levelname)-8s| %(message)s"
        )
        formatter = logging.Formatter(
            fmt=fmt,
        )
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

    else:  # log to console
        fmt = (
            "%(log_color)s%(levelname)-8s%(reset)s| %(filename)s:%(lineno)d | %(message)s"
            if log_level == logging.DEBUG
            else "%(log_color)s%(levelname)-8s%(reset)s| %(message)s"
        )

        colored_formatter = colorlog.ColoredFormatter(
            fmt,
            log_colors={
                "DEBUG": "reset",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
            datefmt="%d-%M-%Y %H:%M:%S,uuu",
        )
        # Create a console handler and set the formatter
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(colored_formatter)

        # Add the console handler to the logger

        logger.addHandler(console_handler)
    logger.setLevel(log_level)


def main():
    # Parse command-line arguments
    version = "0.1.0"
    print(os.path.abspath(__file__))
    print(os.path.abspath(os.path.curdir))
    print(
        os.path.relpath(
            os.path.abspath(__file__), os.path.abspath(os.path.curdir)
        )
        + ":80"
    )
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
