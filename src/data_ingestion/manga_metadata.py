from src.utilities.database_connection import get_collection
from src.utilities.insert_links_metadata import process_and_insert_manga_data
from src.utilities.read_manga_links_csv_db import get_links
from src.utilities.logger_setup import setup_logging


def insert_links_to_db(manga_links=None):
    """Inserts manga links into the database, either from CSV or DB."""
    collection_name = get_collection("get_manga_metadata")
    link_data = [link['manga_url'] for link in manga_links]
    # link_data=['https://mangatx.to/manhua/gods-gambit/']
    log_name = setup_logging(filename="manga_metadata_insert")
    process_and_insert_manga_data(links_list=link_data, collection_name=collection_name, logger=log_name)


if __name__ == "__main__":
    links = get_links(filepath=None, use_db=True)
    insert_links_to_db(links)
    # insert_links_to_db()
