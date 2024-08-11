import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

COLLECTIONS = {
    "get_manga_images": "MANGAIMAGES",
    "get_manga_chapters": "MANGACHAPTERS",
    "get_manga_metadata": "MANGAMETATDATA",
    "get_csv_links": "CSVLINKS",
}


def get_database_connection():
    """Creates a connection to the MongoDB database."""
    try:
        password = os.getenv("MONGODB_PASSWORD")
        username = os.getenv("MONGODB_CLUSTER")
        dbname = os.getenv("MONGODB_DATABASE")
        uri = f"mongodb+srv://mongodb:{password}@{username}.gwrvbi6.mongodb.net/?retryWrites=true&w=majority"
        return MongoClient(uri)[dbname]
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None


def get_collection(collection_name: str, db=None):
    """Fetches a specific collection from the MongoDB database."""
    if db is None:  # Create connection if not provided
        db = get_database_connection()
    collection = os.getenv(COLLECTIONS.get(collection_name))
    if collection:
        return db[collection]
    raise ValueError(
        f"No Collection Found with the name '{collection_name}'. Please check your collection name and try again.")
