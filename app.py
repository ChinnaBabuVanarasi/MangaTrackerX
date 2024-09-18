from fastapi import FastAPI, Body

from src.utilities.mongodb_crud_api import get_records, insert_records, delete_records
from src.models.PostModels import PostLinks
from src.utilities.database_connection import get_collection

app = FastAPI()


@app.get('/api/links')
async def get_all_links():
    records = get_records(endpoint='all_links')
    return records


@app.get('/api/chapters')
async def get_all_metadata():
    records = get_records(endpoint='chapters')
    return records


@app.get('/api/chapter')
async def get_metadata_one(query: str):
    records = get_records(search_key=query, endpoint='chapter')
    return records


@app.post("/api/insert_link")
async def insert_data_to_db(links: PostLinks = Body()):
    validated_data = links.dict()
    result = insert_records(collection_tag=validated_data['tags'], links=validated_data["links"])
    return result

@app.delete("/api/delete_record")
async def delete_records_db(links: PostLinks = Body()):
    validated_data = links.dict()
    result = delete_records(collection_tag=validated_data['tags'], payload=validated_data["links"])
    return result