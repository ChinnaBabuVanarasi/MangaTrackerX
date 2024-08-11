# -*- coding: utf-8 -*-
from src.utilities.database_connection import get_collection


def get_records(search_key=None, endpoint=None):
    collection = get_collection('get_manga_chapters')
    projection = {"_id": False, "en_manga_image": False}
    if endpoint == 'all_links':
        return [record['Manga_url'] for record in list(collection.find({}))]

    elif endpoint == 'chapters':
        return [record for record in list(collection.find({}, projection))]

    elif endpoint == 'chapter':
        query = {"$or": [{"manga_title": search_key}, {"manga_url": search_key}]}
        record = collection.find_one(query, projection)
        if record:
            return record
        else:
            return {"message": "Manga not found"}



