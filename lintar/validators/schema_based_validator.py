import logging
import os

import requests
from lxml import etree


def download_schema(schema_url):
    cache_path = os.path.join(
        os.path.expanduser("~"), ".cache", "lintar", "schema"
    )
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    schema_file = schema_url.split(" ")[-1]
    schema_path = os.path.join(cache_path, schema_file)

    logging.debug(f"Caching schema file at: {cache_path}")
    if os.path.exists(schema_path):
        logging.info(f"Using cached schema file: {cache_path}")
        return schema_path

    try:
        logging.info(f"Downloading schema file from: {schema_url}")
        response = requests.get(schema_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 503:
            logging.error(
                "503 Error: Service Unavailable. Please try again later."
            )
            return None
        else:
            logging.error(f"HTTP Error: {e}")
            return None

    with open(schema_path, "wb") as file:
        file.write(response.content)

    logging.info(f"Schema file downloaded and cached at: {schema_path}")
    return cache_path


def validate_arxml_with_schema(arxml_file):
    if not os.path.exists(arxml_file):
        logging.critical(f"ARXML {arxml_file} file does not exist.")
        exit(-1)

    # Load the ARXML file
    arxml_tree = etree.parse(arxml_file)

    arxml_root = arxml_tree.getroot()
    schema_location = arxml_root.get(
        "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"
    )

    # Download and cache the schema file
    schema_file = schema_location.split(" ")[-1]
    schema_path = download_schema(schema_location)
    if schema_path is None:
        logging.error("Failed to download schema file.")
        logging.info("Trying lo load pre-defined schema file.")
        schema_path = os.path.join(os.path.dirname(__file__), schema_file)

    # Load the schema file
    schema_root = etree.parse(schema_path)
    schema = etree.XMLSchema(schema_root)

    # Validate the ARXML file against the schema
    is_valid = schema.validate(arxml_tree)

    if is_valid:
        logging.info(f"ARXML file {arxml_file} is valid.")
    else:
        logging.error(f"ARXML file {arxml_file} is not valid.")
        logging.error(schema.error_log)
    return is_valid
