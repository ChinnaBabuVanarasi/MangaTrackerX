# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Dict, Any

from fastapi import HTTPException, status

from src.utilities.database_connection import get_collection


def get_date_added():
    current_datetime = datetime.now()
    return datetime(current_datetime.year,
                    current_datetime.month,
                    current_datetime.day
                    )


def get_records(search_key=None, endpoint=None):
    collection = get_collection('get_manga_chapters')
    projection = {"_id": False}

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


def insert_records(records, collection_name):
    collection = get_collection(collection_name)
    response = []
    for record in records:
        query = {"manga_url": record['manga_url']}
        existing_record = collection.find_one(query)
        if not existing_record:
            if isinstance(record, dict):
                try:
                    result = collection.insert_one(record)
                    if result.inserted_id:
                        response.append({"message": f"{record['manga_url']} inserted successfully",
                                         "status_code": status.HTTP_201_CREATED})
                    else:
                        response.append({"message": f"Insertion failed for {record['manga_url']}",
                                         "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR})
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error inserting data: {str(e)}")
            else:
                response.append("No valid entries to insert. Check for unexpected data types in new_entries.")
        else:
            response.append({"message": f"{record['manga_url']} Already present in the Collection - {collection_name}",
                             "status_code": status.HTTP_200_OK})
    return response


def format_records(payload, collection_name: str) -> Any:
    """Inserts data from a list of dictionaries into a specific collection.

    Args:
        payload: A list of dictionaries containing the data to insert.
        collection_name: The name of the collection in the database.

    Returns:
        The response from the `insert_records` function (implementation assumed).
    """

    records = [
        {
            **data,  # Unpack remaining key-value pairs from the original data
            "manga_url": data["manga_url"].rstrip("/"),
            "date_added": get_date_added(),
        }
        for data in payload
    ]
    return insert_records(records=records, collection_name=collection_name)
