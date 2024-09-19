# -*- coding: utf-8 -*-
from datetime import datetime

from fastapi import HTTPException

from src.utilities.database_connection import get_collection


def get_records(search_key=None, endpoint=None):
    collection = get_collection('get_manga_chapters')
    projection = {"_id": False}

    if endpoint == 'all_links':
        return [record['manga_url'] for record in collection.find({}, projection)]

    elif endpoint == 'chapters':
        #  "en_manga_image": False - Optional when testing
        projection = {"_id": False, "latest_chapters": False}
        return [record for record in list(collection.find({}, projection))]

    elif endpoint == 'chapter':
        query = {"$or": [{"manga_title": search_key}, {"manga_url": search_key}]}
        record = collection.find_one(query, projection)
        return record


def get_date_added():
    current_datetime = datetime.now()
    return datetime(current_datetime.year,
                    current_datetime.month,
                    current_datetime.day
                    )


def get_collection_by_tag(collection_tag):
    collection_mapping = {
        'links': 'get_csv_links',
        'metadata': 'get_manga_metadata',
        'chapters': 'get_manga_chapters'
    }
    collection_name = collection_mapping.get(collection_tag, 'default_collection')
    return get_collection(collection_name)


def get_existing_record(collection, query):
    return collection.find_one({'manga_url': query.rstrip('/')}, {"_id": False})


def insert_records(collection_tag=None, links=None):
    response = []
    collection = get_collection_by_tag(collection_tag)
    for query in links:
        if not get_existing_record(collection, query):
            date_added = get_date_added()
            data = {"manga_url": query.rstrip('/'), "date_added": date_added}
            collection.insert_one(data)
            response.append({"status": 200, "message": f"Successfully Inserted url - {query}"})
        else:
            response.append({"status": 200,  "message": "manga url already exists in csv_links Collections"})
    return response


def delete_records(collection_tag=None, payload=None):
    response = []
    collection = get_collection_by_tag(collection_tag)
    for record in payload:
        if get_existing_record(collection, record):
            collection.delete_one({"manga_url": record})
            response.append({"message": f"Successfully Deleted url - {record}"})
        else:
            response.append({"message": f"Manga url does not exist in {collection_tag} Collection"})
    return response
