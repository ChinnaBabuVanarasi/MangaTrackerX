import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from colorama import Fore
from src.utilities.common_functions import setup_logging

from src.utilities.database_connection import get_collection


def get_links_from_csv(filepath):
    """Efficiently reads and extracts links from a CSV."""
    return pd.read_csv(filepath)["links"].tolist()  # Direct conversion to list


def insert_links_to_csv(links_list, collection):
    """Inserts links, handles duplicates, and logs operations."""
    logger = setup_logging(filename="manga_csv_links_insert")

    current_datetime = datetime.now()
    date_added = datetime(
        current_datetime.year, current_datetime.month, current_datetime.day
    )
    new_links = []

    for link in links_list:
        # Efficient check for existence in the collection
        if not collection.find_one({"Manga_url": link}):
            new_links.append({"Manga_url": link, "Date_added": date_added})
            print(Fore.RED, f"Inserted: {link}")

    if new_links:
        collection.insert_many(new_links)  # Bulk insert
        for link in new_links:
            logger.info(f"Inserted Manga_link: {link['Manga_url']}")
    else:
        print(Fore.GREEN, "All links already exist in the database.")


# Main execution
if __name__ == "__main__":
    collection_name = get_collection("get_csv_links")

    # File path handling within the script (no user input needed)
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    csv_file_path = f'{PROJECT_ROOT}/csv_files/manga_links.csv'
    links = get_links_from_csv(csv_file_path)  # Directly get links

    insert_links_to_csv(links, collection_name)
