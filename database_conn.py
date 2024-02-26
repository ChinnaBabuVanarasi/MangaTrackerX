import json
import os
from pymongo import MongoClient

cached_credentials = None


def read_credentials():
    """
    Reads and returns the cached credentials from the "creds.json" file.

    Returns:
        dict: The cached credentials.
    """
    if not hasattr(read_credentials, "cached_credentials"):
        credentials_path = os.path.join(
            os.path.dirname(__file__), ".", "env", "creds.json"
        )
        with open(credentials_path, "r") as f:
            read_credentials.cached_credentials = json.load(f)
    return read_credentials.cached_credentials


def create_database_connection():
    """
    Creates a connection to the database using the credentials obtained from the `read_credentials` function.

    Returns:
        MongoClient: A connection to the MongoDB database.
    """
    credentials = read_credentials()
    password = credentials["PASSWORD"]
    username = credentials["CLUSTER"]
    dbname = credentials["DATABASE"]

    uri = f"mongodb+srv://mongodb:{password}@{username}.gwrvbi6.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    return client[dbname]



def get_collection(collection_name: str):
    """
    Retrieves a collection from the database based on the given collection name.

    Args:
        collection_name (str): The name of the collection to retrieve.

    Returns:
        pymongo.collection.Collection: The collection object corresponding to the given collection name.

    Raises:
        str: If no collection is found with the given collection name.
    """
    credentials = read_credentials()
    db_connection = create_database_connection()
    if collection_name == "get_manga_links":
        collection = credentials["MANGALINKS"]
    elif collection_name == "get_manga_details":
        collection = credentials["MANGADETAILS"]
    elif collection_name == "get_manga_images":
        collection = credentials["MANGAIMAGES"]
    elif collection_name == "get_chapters":
        collection = credentials["CHAPTERSDB"]
    elif collection_name == "get_csv_links":
        collection = credentials["CSVLINKS"]
    else:
        return "No Collection Found with that {collection_name} name. Please check your collection name and try again."
    return db_connection[collection]

# get_collection('get_manga_links') # get_manga_links()
# get_collection('get_latest_chapter')
