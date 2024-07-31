import logging
import os
from pathlib import Path

from src.utilities.database_connection import get_collection
from src.utilities.insert_links_metadata import process_and_insert_manga_data
from src.utilities.read_manga_links_csv_db import get_links
from src.utilities.logger_setup import setup_logging


def insert_links_to_csv():
    collection_name = get_collection("get_csv_links")

    # File path handling within the script (no user input needed)
    file_path = os.path.join(Path(os.getcwd()).parent.parent.resolve(), "csv_files/manga_links.csv")
    use_database = False  # Set to True if reading from the database
    links = get_links(filepath=file_path if not use_database else None, use_db=use_database)
    log_name = setup_logging(filename='csv_links_ingestion', log_level=logging.DEBUG)
    process_and_insert_manga_data(links_list=links, collection_name=collection_name, logger=log_name)


# Main execution
if __name__ == "__main__":
    insert_links_to_csv()
