from validators import url

try:
    from src.utilities.database_connection import get_collection
except ModuleNotFoundError:
    from database_connection import get_collection


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
            result = collection.update_one({"Title": title}, {
                "$set": {"Image": manga["Image"], "Binary_Image": manga["Binary_Image"],
                         "Manga_url": manga["Manga_url"], },
                "$addToSet": {"Latest_chapters": {"$each": sorted_chapters}, }, }, upsert=True, )
            # Using addToSet to avoid duplicate chapters # Insert if document doesn't exist

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
