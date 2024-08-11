import re
import time
from datetime import datetime

from colorama import Fore

from src.utilities.database_connection import get_collection
from src.utilities.insert_chapters import insert_chapters_data
from src.utilities.logger_setup import setup_logging
from src.utilities.page_source import get_page_source, get_date_added

chapter_logger = setup_logging(filename="chapters_logger")  # Combined logger


def get_latest_chapter(chapter):
    """Efficiently extracts the latest chapter number from a chapter element."""
    chapter_text = chapter.find("a").text.strip()
    chapter_num_str = re.findall(r"\d+\.\d+|\d+", chapter_text)[-1]  # Get last number
    return float(chapter_num_str) if "." in chapter_num_str else int(chapter_num_str)


def get_chapters(manga_url, current_chapter, manga_title):
    """Gets new chapter details since the last recorded chapter."""
    soup = get_page_source(manga_url)

    # Combined chapter finding logic:
    if soup.find("div", class_="page-content-listing.single-page"):
        chapters = soup.find("div", class_="page-content-listing.single-page").findAll("li", class_="wp-manga-chapter")
    else:
        chapters = soup.findAll("li", class_="wp-manga-chapter")

    # Optimization: Stop iteration once the current chapter is found
    new_chapters = []
    for chapter in chapters:
        latest_chapter = get_latest_chapter(chapter)
        if float(latest_chapter) == float(current_chapter):
            break  # No need to check further

        new_chapters.append({
            "chapter_num": latest_chapter,
            "chapter_url": chapter.find("a")["href"],
            "chapter_added": get_date_added(),
        })

    log_message = (
        f"New chapters for '{manga_title}': {current_chapter} -> {new_chapters[0]['chapter_num'] if new_chapters else current_chapter}" if new_chapters
        else f"No new chapters for '{manga_title}': {current_chapter}"
    )
    chapter_logger.info(log_message)
    return new_chapters


def extract_chapters():
    """Extracts chapter details, updates the database, and handles errors."""
    chapter_collection = get_collection("get_manga_chapters")
    manga_details_collection = get_collection("get_manga_metadata")

    for i, record in enumerate(manga_details_collection.find({})):
        url = record["manga_url"]
        existing_record = chapter_collection.find_one({"manga_url": url})
        current_chapter = float(existing_record["latest_chapters"][0]["chapter_num"]) if existing_record else 0
        new_chapters = get_chapters(url, current_chapter, record["manga_title"])
        if new_chapters:
            insert_chapters_data(new_chapters=new_chapters,
                                 current_chapter=current_chapter,
                                 chapter_collection=chapter_collection, record=record)
            print(Fore.GREEN, f"{i}: Inserted: {url}")
        else:
            print(Fore.RED, f"{i}: No new Chapters for: {url}")
        time.sleep(1)


if __name__ == "__main__":
    extract_chapters()
