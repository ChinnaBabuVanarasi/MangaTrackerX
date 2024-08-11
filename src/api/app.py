from urllib.parse import unquote

from fastapi import FastAPI
from fastapi import FastAPI

from src.utilities.mongodb_crud_api import get_records

app = FastAPI()


@app.get('/api/links')
async def get_all_links():
    records = get_records(endpoint='all_links')
    links = [record['manga_url'] for record in records]
    return links


@app.get('/api/chapters')
async def get_all_metadata():
    records = get_records(endpoint='chapters')
    return records


@app.get('/api/chapter')
async def get_metadata_one(query: str):
    records = get_records(search_key=query, endpoint='chapter')
    return records
