import logging
import os
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from validators import url

try:
    from src.utilities.database_connection import get_collection
except ModuleNotFoundError:
    from database_connection import get_collection


# load_dotenv()

# # MongoDB Configuration (Assumes you have loaded env variables)
# MONGODB_URI = os.getenv("MONGODB_URI")  # Get MongoDB connection URI from environment
# DB_NAME = os.getenv("MONGODB_DATABASE")
#
# # Global MongoClient for connection pooling
# client = MongoClient(MONGODB_URI)
# db = client[DB_NAME]


def setup_logging(filename):
    if "chapter" in filename:
        filename = f"Chapters/{filename}"
        name = filename.split("/")[1].split("_logger")[0]
    else:
        filename = filename
        name = filename.split("_logger")[0]
    try:
        log_directory = os.path.join(Path(os.getcwd()).resolve(), 'logs')
    except FileNotFoundError:
        log_directory = r"C:\\Users\\chinn\\PycharmProjects\\MangaTrackerX\\logs"
    log_file_name = os.path.join(
        f"{log_directory}/{filename}",
        f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
    )
    os.makedirs(os.path.dirname(log_file_name), exist_ok=True)

    # Create a logger instance
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create a file handler
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.INFO)

    # Create a log format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger


def get_page_source(manga_url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537"
    )
    driver = webdriver.Chrome(options=options)
    driver.get(manga_url)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    return soup


def mongodb_insertion(manga_details, collection_name, insert_logger):
    """
    Inserts or updates manga details into a MongoDB collection.
    """
    collection = get_collection(collection_name)  # Get collection from the database

    for manga in manga_details:
        try:
            title = manga["Title"]
            local_latest_chapters = manga.get("Latest_chapters", [])

            sorted_chapters = sorted(local_latest_chapters, key=lambda x: x.get("chapter_num", 0), reverse=True)

            # Find the document based on the title and update it
            result = collection.update_one(
                {"Title": title},
                {
                    "$set": {
                        "Image": manga["Image"],
                        "Binary_Image": manga["Binary_Image"],
                        "Manga_url": manga["Manga_url"],
                    },
                    "$addToSet": {  # Using addToSet to avoid duplicate chapters
                        "Latest_chapters": {"$each": sorted_chapters},
                    },
                },
                upsert=True,  # Insert if document doesn't exist
            )

            if result.matched_count > 0:
                insert_logger.info(f"Updated existing document for '{title}' in MongoDB.")
            else:
                insert_logger.info(f"Inserted new document for '{title}' into MongoDB.")
        except Exception as e:
            insert_logger.error(f"Error occurred for manga: {manga.get('Title', 'Unknown')}. Error: {e}")


class InvalidMangaDataError(ValueError):
    pass


class InvalidChapterDataError(ValueError):
    pass


def validate_data(manga_details):
    for manga in manga_details:
        if not isinstance(manga["Title"], str) or not manga["Title"].strip():
            raise InvalidMangaDataError("Invalid Title (must be a non-empty string)")
        if not isinstance(manga["Image"], str):
            raise ValueError("Invalid Image")
        if not isinstance(manga["Binary_Image"], str):
            raise ValueError("Invalid Binary_Image")
        if not isinstance(manga["Latest_chapters"], list):
            raise InvalidMangaDataError("Invalid Latest_chapters (must be a list)")
        for chapter in manga["Latest_chapters"]:
            if not isinstance(chapter["chapter_num"], int):
                raise InvalidChapterDataError("Invalid chapter_num (must be an integer)")
            if not isinstance(chapter["chapter_url"], str) or not url(chapter["chapter_url"]):
                raise InvalidChapterDataError("Invalid chapter_url (must be a valid URL)")
