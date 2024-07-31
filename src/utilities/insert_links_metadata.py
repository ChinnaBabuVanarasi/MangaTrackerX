import base64
import os
import time
from pathlib import Path

import requests
from colorama import Fore
from pymongo.errors import PyMongoError

from src.utilities.database_connection import get_collection
from src.utilities.read_manga_links_csv_db import get_summary_content
from src.utilities.page_source import get_date_added, get_page_source

IMAGE_CONSTANT = "/9j/4QVfRXhpZgAASUkqAAgAAAAMAAABAwABAAAALAEAAAEBAwABAAAAwgEAAAIBAwADAAAAngAAAAYBAwABAAAAAgAAABIBAwAB"


def get_image(soup, manga_title):
    """Fetches and processes image data from the manga page."""
    image_link = soup.find("div", class_="tab-summary").find("a")

    # Find the <img> tag with 'srcset' attribute
    img_with_srcset = image_link.find("img", {"srcset": True})

    # If found, get the first image source from the 'srcset' attribute
    if img_with_srcset:
        image_src = img_with_srcset.get("srcset").split(",")[0]
    else:
        # Otherwise, find the <img> tag with 'data-src' or 'src' attributes
        img_with_data_src = image_link.find("img", {"data-src": True})
        img_with_src = image_link.find("img", {"src": True})

        # Get the 'data-src' or 'src' value, whichever is found first
        image_src = img_with_data_src.get("data-src") if img_with_data_src else img_with_src.get("src")

    # If no image source is found, set image_src to None (or a default value)
    image_src = image_src or None

    image_url = image_src if " " not in image_src else image_src.split(" ")[0]

    try:
        response = requests.get(image_url)
        if response.status_code != 200:
            raise requests.exceptions.RequestException(
                f"Failed to fetch image: {response.status_code}"
            )
        image_data = response.content
        en_manga_image = base64.b64encode(image_data).decode("utf-8")
        return {
            "image": image_url,
            "en_manga_image": en_manga_image
            if en_manga_image[:100] != IMAGE_CONSTANT
            else get_collection("get_manga_images").find_one({"manga_title": manga_title}).get("en_manga_image",
                                                                                               en_manga_image),
        }
    except requests.exceptions.RequestException:
        placeholder_image_url = os.path.join(
            Path(os.getcwd()).resolve().parent.parent, "assets/images/placeholder.jpg"
        )
        with open(placeholder_image_url, "rb") as f:
            image_data = f.read()
        return {
            "image": None,
            "en_manga_image": base64.b64encode(image_data).decode("utf-8"),
        }

def process_and_insert_manga_data(links_list, collection_name, logger):
    """Processes manga links, extracts details if necessary, and inserts them into the database.

    Args:
        links_list (list or dict): A list of manga URLs or a dictionary of URLs with 'Date_added' keys.
        collection_name: The MongoDB collection to insert into.
        logger: the log file of calling function
    """
    new_entries = []
    for i, item in enumerate(links_list):
        try:
            # Process based on item type
            if isinstance(item, str):  # Single link from list
                link = item
                if not collection_name.find_one({"manga_url": link}):
                    # Extract details and create data dictionary
                    soup = get_page_source(link)
                    data = extract_manga_data(soup, link)
                    new_entries.append(data)
                    time.sleep(5)  # Adjust sleep time as needed

            elif isinstance(item, dict):  # Dictionary with 'manga_url' and possibly 'Date_added'
                link = item["manga_url"]
                if not collection_name.find_one({"manga_url": link}):
                    # Create basic entry with 'manga_url' and 'date_added'
                    new_entries.append(dict(manga_url=link, date_added=get_date_added()))

            else:
                raise ValueError(Fore.RED + f"Invalid item type: {type(item)}")

            print(Fore.GREEN + f"{i}: Inserted: {link}")
            logger.info(f"Inserted: {link}")

        except (KeyError, ValueError) as e:
            logger.error(f"Error processing item {i}: {item} - {e}")  # Use error level for non-critical issues
        except PyMongoError as e:
            logger.critical(f"MongoDB error inserting: {item} - {e}")  # Use critical level for serious errors

    if new_entries:
        try:
            collection_name.insert_many(new_entries)
        except PyMongoError as e:
            logger.critical(f"MongoDB error during bulk insert: {e}")
    else:
        print(Fore.GREEN, "All links/entries already exist in the database.")


# Define a separate function for extracting manga details (assuming you have functions like get_page_source, get_image, etc.)
def extract_manga_data(soup, link):
    title = soup.find("div", class_="post-title").find("h1").text.strip()
    site = link.split("/")[2]
    image_data = get_image(soup, title)
    dic = get_summary_content(soup=soup)
    manga_rating, manga_genre, manga_type, manga_release, manga_status = (dic['rating'],
                                                                          dic['genre(s)'], dic['type'],
                                                                          dic['release'], dic['status'])
    data = {
        "manga_title": title,
        "manga_site": site,
        "manga_url": link,
        "manga_image": image_data["image"],
        "en_manga_image": image_data["en_manga_image"],
        "manga_rating": manga_rating,
        "manga_genre": manga_genre,
        "manga_type": manga_type,
        "manga_release": manga_release,
        "manga_status": manga_status,
        "date_added": get_date_added(),
    }
    return data
