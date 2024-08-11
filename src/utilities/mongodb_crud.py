# -*- coding: utf-8 -*-
from src.utilities.database_connection import get_collection


def find_and_delete_by_url(collection_name):
    """Finds a record by URL, presents it, and then deletes it."""
    collection = get_collection(collection_name)
    urls = get_records_urls_in_col(collection_name)
    for url in urls:
        if url == "https://kunmanga.com/manga/children-of-the-rune/":
            print(url)
            # Delete the record
            result = collection.delete_one({"Manga_url": url})
            if result.deleted_count == 1:
                print("Record deleted successfully")
            else:
                print("Error deleting record")
        else:
            print("Record not found")


def delete_one_by_url(collection_name):
    """Finds a record by URL, presents it, and then deletes it."""
    collection = get_collection(collection_name)
    url = "https://kunmanga.com/manga/children-of-the-rune/"
    # Delete the record
    result = collection.delete_one({"Manga_url": url})
    if result.deleted_count == 1:
        print("Record deleted successfully")
    else:
        print("Error deleting record")


def get_records_urls_in_col(collection_name):
    collection = get_collection(collection_name)
    records = [record['Manga_url'] for record in list(collection.find({}))]
    return records


def get_records(collection_name, search_key=None, projection=None):
    collection = get_collection(collection_name)
    if projection is None:
        projection = {"_id": False, "en_manga_image": False}
    if search_key is None:
        records = collection.find({}, projection)
    else:
        print(search_key)
        query = {"$or": [{"manga_title": search_key}, {"manga_url": search_key}]}
        print(query)
        records = collection.find_one(query, projection)
    return records


def find_unique_elements(links, meta, chap):
    set1, set2, set3 = set(links), set(meta), set(chap)
    #
    unique_to_list1 = set1 - (set2 | set3)
    unique_to_list2 = set2 - (set1 | set3)
    unique_to_list3 = set3 - (set1 | set2)
    print("links: ", unique_to_list1)
    print("meta: ", unique_to_list2)
    print("chap: ", unique_to_list3)


def update_manga_urls(collection_name):
    collection = get_collection(collection_name)
    for doc in collection.find():
        manga_url = doc.get("manga_url")
        if manga_url and manga_url.endswith("/"):
            new_manga_url = manga_url[:-1]  # Remove the trailing slash
            collection.update_one({"_id": doc["_id"]}, {"$set": {"manga_url": new_manga_url}})


chapters_col = 'get_manga_chapters'
metadata_col = 'get_manga_metadata'
links_col = 'get_csv_links'
# find_and_delete_by_url(collection_name=chapters_col)
# list1 = get_records_urls_in_col(links_col)
# list2 = get_records_urls_in_col(metadata_col)
# list3 = get_records_urls_in_col(chapters_col)
# find_unique_elements(list1, list2, list3)

# manga_title = "Academy’s Genius Swordmaster"
# record2 = get_records(collection_name='get_manga_chapters', search_key=manga_title)
# print(record2)
update_manga_urls(links_col)
