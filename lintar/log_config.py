import logging

import colorlog


def configure_logger(log_file=None, log_level=logging.INFO):
    """
    Configure the logger with a console handler and an optional file handler.
    This configuration:
    - redirects logging to console OR file
    - log code origin is added to the log message only for DEBUG level
    - timestamp is added to the log message only when logging to file

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
            "%(asctime)s| %(levelname)-8s"
            + "| %(filename)s:%(lineno)d | %(message)s"
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
            "%(log_color)s%(levelname)-8s%(reset)s"
            + "| %(filename)s:%(lineno)d | %(message)s"
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
