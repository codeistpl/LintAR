import argparse
import logging

import colorlog
from validators.schema_based_validator import validate_arxml_with_schema


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

    # Create a color formatter
    formatter = colorlog.ColoredFormatter(
        "%(asctime)s %(log_color)s%(levelname)-8s"
        + "%(reset)s %(filename)s::%(lineno)d - %(message)s",
        log_colors={
            "DEBUG": "reset",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
        datefmt="%d-%M-%Y %H:%M:%S",
    )

    # Create a console handler and set the formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger = logging.getLogger()
    logger.addHandler(console_handler)
    logger.setLevel(log_level)

    # Check if log_file is provided
    if log_file:
        # Create a file handler and set the formatter
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)


def main():
    # Parse command-line arguments
    version = "0.1.0"
    parser = argparse.ArgumentParser(
        description="LintAR the ARXML linting tool"
    )
    parser.add_argument(
        "file", metavar="FILE", type=str, help="Path to the input file"
    )
    parser.add_argument(
        "--log-level", default="INFO", help="Set the log level (default: INFO)"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {version}"
    )

    args = parser.parse_args()

    # Set up logging
    configure_logger(log_level=args.log_level)
    if validate_arxml_with_schema(args.file) is False:
        exit(1)


if __name__ == "__main__":
    main()
